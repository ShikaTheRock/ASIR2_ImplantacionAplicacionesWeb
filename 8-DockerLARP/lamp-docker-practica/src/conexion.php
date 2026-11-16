
<?php

$host = getenv('DB_HOST');
$database = getenv('DB_NAME');
$user = getenv('DB_USER');
$password = getenv('DB_PASSWORD');

$conexion = new mysqli(
    $host,
    $user,
    $password,
    $database
);

if ($conexion->connect_error) {
    die("Error de conexión: " . $conexion->connect_error);
}

$conexion->set_charset("utf8mb4");

// Insertar un alumno de prueba
$nombre = "Alumno de prueba";
$email = "alumno@prueba.com";

$stmt = $conexion->prepare(
    "INSERT INTO alumnos (nombre, email) VALUES (?, ?)"
);

$stmt->bind_param("ss", $nombre, $email);
$stmt->execute();
$stmt->close();

// Consultar los alumnos
$resultado = $conexion->query(
    "SELECT * FROM alumnos ORDER BY id DESC"
);

?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Conexión LAMP</title>
</head>
<body>

<h1>Conexión PHP - MariaDB correcta</h1>

<p>Conectado al servidor: <?= htmlspecialchars($host) ?></p>

<h2>Alumnos registrados</h2>

<table border="1" cellpadding="8">
    <tr>
        <th>ID</th>
        <th>Nombre</th>
        <th>Email</th>
    </tr>

    <?php while ($fila = $resultado->fetch_assoc()): ?>
    <tr>
        <td><?= htmlspecialchars($fila['id']) ?></td>
        <td><?= htmlspecialchars($fila['nombre']) ?></td>
        <td><?= htmlspecialchars($fila['email']) ?></td>
    </tr>
    <?php endwhile; ?>

</table>

</body>
</html>

<?php
$conexion->close();
?>
