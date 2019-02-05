<?php

declare(strict_types=1);

$relName = $_GET['service'];

$relationships = json_decode(base64_decode(getenv('PLATFORM_RELATIONSHIPS')), TRUE);

if (empty($relationships[$relName])) {
    return;
}

// Cache real output for 5 minutes.
header('cache-control: public max-age=300');

print \json_encode($relationships[$relName][0], JSON_PRETTY_PRINT);
