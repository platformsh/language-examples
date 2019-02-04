<?php

declare(strict_types=1);

$relName = $_GET['service'];

$relationships = json_decode(base64_decode(getenv('PLATFORM_RELATIONSHIPS')), TRUE);


if (empty($relationships[$relName])) {
    return;
}

print \json_encode($relationships[$relName], JSON_PRETTY_PRINT);
