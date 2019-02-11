<?php

declare(strict_types=1);

require __DIR__.'/../vendor/autoload.php';


function capture_output(callable $callable) {
    ob_start();
    $callable();
    $contents = ob_get_contents();
    ob_end_clean();
    return $contents;
}

function handleRequest(string $path)
{
    $routes = routeList();

    if (!isset($routes[$path])) {
        print 'Sorry, no sample code is available.';
        return;
    }

    print $routes[$path]();
}

function debug($var) : void
{
    $val = print_r($var, true);

    print "<div style='display:none'>{$val}</div>\n";
}

function routeList() : array
{
    $routes = [];

    $routes['/'] = function() {
        return capture_output(function() {
            require 'list.php';
        });
    };

    $files = glob("../examples/*.php");

    foreach ($files as $filename) {
        $file = basename($filename, '.php');
        $path = strtolower($file);
        $routes['/' . $path] = function() use ($filename) {
            return file_get_contents($filename);
        };
        $routes["/{$path}/output"] = function() use ($filename) {
            return capture_output(function() use ($filename) {
                include $filename;
            });
        };
    }
    return $routes;
}

handleRequest($_SERVER['REQUEST_URI']);
