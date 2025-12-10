<?php
$configPath = __DIR__ . "/config.json";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = [
        "source_url" => $_POST['source_url'] ?? "",
        "ftp_host" => $_POST['ftp_host'] ?? "",
        "ftp_username" => $_POST['ftp_username'] ?? "",
        "ftp_password" => $_POST['ftp_password'] ?? "",
        "ftp_target_path" => $_POST['ftp_target_path'] ?? ""
    ];

    file_put_contents($configPath, json_encode($data, JSON_PRETTY_PRINT));
    echo "Configuration saved successfully!";
    exit;
}
?>

<form method="POST">
    <label>Source Feed URL:</label><br>
    <input type="text" name="source_url" required><br>

    <label>FTP Host:</label><br>
    <input type="text" name="ftp_host" required><br>

    <label>FTP Username:</label><br>
    <input type="text" name="ftp_username" required><br>

    <label>FTP Password:</label><br>
    <input type="password" name="ftp_password" required><br>

    <label>Target File Name:</label><br>
    <input type="text" name="ftp_target_path" required><br><br>

    <button type="submit">Save Config</button>
</form>
