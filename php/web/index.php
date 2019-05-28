<?php

declare(strict_types=1);

use Platformsh\ConfigReader\Config;

require __DIR__.'/../vendor/autoload.php';


function capture_output(callable $callable) {
    ob_start();
    $callable();
    $contents = ob_get_contents();
    ob_end_clean();
    return $contents;
}


/**
 * Makes a callable routine exclusively locked, aka "synchronized".
 *
 * @param string $lockname
 *   The name of the lock. Will be used as a filename.
 * @param callable $callable
 *   The routine to make synchronous.
 * @return mixed
 */
function lock_exclusive(string $lockname, callable $callable) {
    $fp = fopen(sys_get_temp_dir() . '/php-locks/' . $lockname, 'r');
    flock($fp, LOCK_EX);
    try {
        return $callable();
    }
    finally {
        flock($fp, LOCK_UN);
    }
}

function handleRequest(string $path) : void
{
    try {
        $router = buildRouter();

        print $router->match($path)();
    }
    catch (InvalidArgumentException $e) {
        print 'Sorry, no sample code is available.';
    }
}

function debug($var) : void
{
    $val = print_r($var, true);

    print "<div style='display:none'>{$val}</div>\n";
}

class NanoRouter
{
    protected $basePath = '';

    protected $routes;

    public function __construct(string $basePath = '')
    {
        $this->basePath = '/' . trim($basePath, '/');
    }

    public function addRoute(string $path, callable $callable) : self
    {
        $path = trim($path, '/');
        $realPath = rtrim(implode('/', [$this->basePath, $path]), '/');

        $this->routes[$realPath] = $callable;

        return $this;
    }

    public function match(string $path) : callable
    {
        $path = rtrim($path, '/');

        if (!isset($this->routes[$path])) {
            throw new \InvalidArgumentException(sprintf('No route found: %s', $path));
        }

        return $this->routes[$path];
    }
}

function buildRouter() : NanoRouter
{
    $platformRoute = (new Config())->getRoute('php');
    $basePath = trim(parse_url($platformRoute['url'], PHP_URL_PATH), '/');

    $router = new NanoRouter($basePath);

    $files = glob("../examples/*.php");

    $default = function() {
        return capture_output(function() {
            require 'list.php';
        });
    };

    $router->addRoute('/', $default);
    $router->addRoute('/index.php', $default);

    foreach ($files as $filename) {
        $path = strtolower(basename($filename, '.php'));

        $router->addRoute($path, function() use ($filename) {
            header('Content-Type: text/plain', true);
            return file_get_contents($filename);
        });
        $router->addRoute($path . '/output', function() use ($filename) {
            header('Content-Type: text/plain', true);
            return capture_output(function() use ($filename) {
                include $filename;
            });
        });
    }

    return $router;
}

handleRequest($_SERVER['REQUEST_URI']);
