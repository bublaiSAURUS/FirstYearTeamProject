<!DOCTYPE html>
<html lang ="en">
<head>
    <link rel="stylesheet" type="text/css" href="/resources/css/myStyles.css">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato&family=Zen+Dots&display=swap" rel="stylesheet">
    <title>Wolfram Beeta</title>
</head>
    <body>
        <div class="header">
            <img id="logo" src="/resources/images/logo.png" alt="website logo">
            <h2 id="brand_name">Wolfram <span style="color: #FFAA00;">Beeta</span></h2>
        </div>
        <navbar>
            <ul>
                <li><a  href="/">Home</a></li>
                <li><a class="active" href="solve">Solve</a></li>
                <li><a href="docs">Docs</a></li>
            </ul>
        </navbar>
        <main>
            <?php
            $variables = $_COOKIE["variables"];
            $constants = $_COOKIE["constants"];
            ini_set('display_errors', '1');
            $host = "dbhost.cs.man.ac.uk";
            $username = "g89496oe";
            $password = "esabatad";
            $dbName = "2022_comp10120_m6";
            try
            {
            $conn = new PDO("mysql:host=$host", $username, $password);
            }
            catch (PDOException $pe)
            {
            die("Could not connect to $host :" . $pe->getMessage());
            }
            $sql = "CREATE TABLE IF NOT EXISTS linear_input (
            recordID INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            variables VARCHAR(120) NOT NULL,
            constants VARCHAR(120) NOT NULL)";
            $pdo = new pdo('mysql:host=' . $host . ';dbname=' . $dbName, $username, $password);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING);
            $pdo->query($sql);
            $sql = "INSERT INTO linear_input (variables,constants) VALUES (:variables,:constants)";
            $stmt = $pdo->prepare($sql);
            $stmt->execute([
            'variables' => $variables,
            'constants' => $constants,
            ]);
            ?>
        </main>
    </body>
</html>