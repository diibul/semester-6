<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Error</title>
    <style>
        body { font-family: "Segoe UI", Tahoma, sans-serif; margin: 0; background: radial-gradient(circle at 20% 20%, #1f2937, #0b1020 50%); color: #e5e7eb; }
        .wrap { min-height: 100vh; display: grid; place-items: center; padding: 24px; }
        .card { width: 100%; max-width: 560px; background: rgba(17, 24, 39, 0.92); border: 1px solid #334155; border-radius: 16px; padding: 28px; box-shadow: 0 20px 45px rgba(2, 6, 23, 0.35); }
        .code { margin: 0; font-size: 13px; letter-spacing: 0.16em; text-transform: uppercase; color: #67e8f9; }
        .title { margin: 0 0 8px; font-size: 28px; }
        .desc { margin: 0 0 20px; color: #9ca3af; line-height: 1.6; }
        a { color: #22d3ee; text-decoration: none; font-weight: 600; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="wrap">
        <div class="card">
            <p class="code">Error 500</p>
            <h1 class="title">500 - Terjadi Gangguan</h1>
            <p class="desc">Sistem sedang mengalami kendala sementara. Silakan coba beberapa saat lagi atau kembali ke halaman utama.</p>
            <a href="{{ url('/') }}">Kembali ke Home</a>
        </div>
    </div>
</body>
</html>
