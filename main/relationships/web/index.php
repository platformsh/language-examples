<?php

declare(strict_types=1);

function debug($var) : void
{
    $val = print_r($var, true);

    print "<div style='display:none'>{$val}</div>\n";
}

function getRelName($requestUrl) : string
{
    $parts = array_filter(explode('/', $requestUrl));
    $rel = array_pop($parts);

    return $rel == 'relationships' ? '' : $rel;
}


function handleRequest($requestUrl)
{
    $relName = getRelName($requestUrl);

    if (!$relName) {
        print "No service specified.";
        return;
    }

    $relationships = json_decode(base64_decode(getenv('PLATFORM_RELATIONSHIPS')), TRUE);

    if (empty($relationships[$relName])) {
        print "No such service: {$relName}";
        return;
    }

    // Cache real output for 5 minutes.
    header('cache-control: public max-age=300');
    print \json_encode($relationships[$relName][0], JSON_PRETTY_PRINT);
}

handleRequest($_SERVER['REQUEST_URI']);

