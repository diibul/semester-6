<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found</title>
    <style>
        body { font-family: "Segoe UI", Tahoma, sans-serif; margin: 0; background: radial-gradient(circle at 20% 20%, #1e293b, #0f172a 50%); color: #e2e8f0; }
        .wrap { min-height: 100vh; display: grid; place-items: center; padding: 24px; }
        .card { width: 100%; max-width: 560px; background: rgba(17, 24, 39, 0.9); border: 1px solid #334155; border-radius: 16px; padding: 28px; box-shadow: 0 20px 45px rgba(2, 6, 23, 0.35); }
        .code { margin: 0; font-size: 13px; letter-spacing: 0.16em; text-transform: uppercase; color: #67e8f9; }
        .title { margin: 0 0 8px; font-size: 28px; }
        .desc { margin: 0 0 20px; color: #94a3b8; line-height: 1.6; }
        a { color: #22d3ee; text-decoration: none; font-weight: 600; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="wrap">
        <div class="card">
            <p class="code">Error 404</p>
            <h1 class="title">404 - Page Not Found</h1>
            <p class="desc">Halaman yang Anda cari tidak tersedia atau sudah dipindahkan. Periksa kembali URL atau kembali ke beranda.</p>
            <a href="{{ url('/') }}">Kembali ke Home</a>
        </div>
    </div>
</body>
</html>
