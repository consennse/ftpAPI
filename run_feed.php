
<?php
$configPath = __DIR__ . "/config.json";

if (!file_exists($configPath)) {
    echo "No configuration found!";
    exit;
}

$config = json_decode(file_get_contents($configPath), true);

$url = "https://ftpapi-wjo8.onrender.com/run";

$options = [
    "http" => [
        "header"  => "Content-type: application/json\r\n",
        "method"  => "POST",
        "content" => json_encode($config)
    ]
];

$context = stream_context_create($options);
$result = file_get_contents($url, false, $context);

echo "Python API Response: " . $result;
?>
