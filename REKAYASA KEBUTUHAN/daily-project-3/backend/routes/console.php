<?php

use App\Models\Alumni;
use Carbon\Carbon;
use Illuminate\Foundation\Inspiring;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Str;

Artisan::command('inspire', function () {
    $this->comment(Inspiring::quote());
})->purpose('Display an inspiring quote');

Artisan::command('alumni:import-csv {path : Path file CSV} {--delimiter= : Delimiter CSV (opsional)} {--dry-run : Validasi tanpa simpan ke database}', function () {
    $path = (string) $this->argument('path');

    if (! is_file($path)) {
        $this->error("File tidak ditemukan: {$path}");

        return self::FAILURE;
    }

    $handle = fopen($path, 'r');
    if ($handle === false) {
        $this->error('Gagal membuka file CSV.');

        return self::FAILURE;
    }

    $delimiter = $this->option('delimiter');
    if (! is_string($delimiter) || $delimiter === '') {
        $previewLine = fgets($handle);
        rewind($handle);
        $delimiter = substr_count((string) $previewLine, ';') > substr_count((string) $previewLine, ',') ? ';' : ',';
    }

    $rawHeaders = fgetcsv($handle, 0, $delimiter);
    if ($rawHeaders === false) {
        fclose($handle);
        $this->error('Header CSV tidak terbaca.');

        return self::FAILURE;
    }

    $normalize = static function (?string $value): string {
        $value = (string) $value;
        $value = preg_replace('/^\xEF\xBB\xBF/', '', $value) ?? $value;
        $value = Str::lower(trim($value));
        $value = preg_replace('/[^a-z0-9]+/', '_', $value) ?? $value;

        return trim($value, '_');
    };

    $headerMap = [
        'nama_lulusan' => 'name',
        'nim' => 'nim',
        'tahun_masuk' => 'entry_year',
        'tanggal_lulus' => 'graduation_date',
        'fakultas' => 'faculty',
        'program_studi' => 'study_program',
        'alamat_sosial_media_linkedin_ig_fb_tiktok' => 'social_media_bundle',
        'email' => 'email',
        'no_hp' => 'phone_number',
        'tempat_bekerja' => 'workplace_name',
        'alamat_bekerja' => 'workplace_address',
        'posisi' => 'position',
        'pns_swasta_wirausaha' => 'employment_type',
        'alamat_sosial_media_tempat_bekerja' => 'workplace_social_media',
    ];

    $headers = array_map(function ($header) use ($normalize, $headerMap) {
        $key = $normalize($header);

        return $headerMap[$key] ?? $key;
    }, $rawHeaders);

    $requiredHeaders = ['name', 'nim', 'study_program'];
    $missingHeaders = array_values(array_diff($requiredHeaders, $headers));
    if ($missingHeaders !== []) {
        fclose($handle);
        $this->error('Header wajib belum ada: '.implode(', ', $missingHeaders));

        return self::FAILURE;
    }

    $parseDate = static function (?string $date): ?string {
        if ($date === null || trim($date) === '') {
            return null;
        }

        $date = trim($date);

        $dateLower = Str::lower($date);
        $monthMap = [
            'januari' => 'january',
            'februari' => 'february',
            'maret' => 'march',
            'april' => 'april',
            'mei' => 'may',
            'juni' => 'june',
            'juli' => 'july',
            'agustus' => 'august',
            'september' => 'september',
            'oktober' => 'october',
            'november' => 'november',
            'desember' => 'december',
        ];
        $dateNormalized = strtr($dateLower, $monthMap);

        $formats = ['Y-m-d', 'd/m/Y', 'm/d/Y', 'd-m-Y', 'd F Y', 'j F Y'];

        foreach ($formats as $format) {
            try {
                return Carbon::createFromFormat($format, $dateNormalized)->format('Y-m-d');
            } catch (\Throwable) {
                // Try next format.
            }
        }

        try {
            return Carbon::parse($dateNormalized)->format('Y-m-d');
        } catch (\Throwable) {
            return null;
        }
    };

    $normalizeEmploymentType = static function (?string $type): ?string {
        if ($type === null) {
            return null;
        }

        $value = Str::lower(trim($type));
        if ($value === '') {
            return null;
        }

        if (Str::contains($value, 'pns')) {
            return 'PNS';
        }

        if (Str::contains($value, 'swasta')) {
            return 'Swasta';
        }

        if (Str::contains($value, 'wirausaha')) {
            return 'Wirausaha';
        }

        return null;
    };

    $extractSocialMedia = static function (?string $bundle): array {
        $result = [
            'social_media_linkedin' => null,
            'social_media_instagram' => null,
            'social_media_facebook' => null,
            'social_media_tiktok' => null,
        ];

        if ($bundle === null || trim($bundle) === '') {
            return $result;
        }

        preg_match_all('/https?:\/\/[^\s,;]+/i', $bundle, $matches);
        $urls = $matches[0] ?? [];

        foreach ($urls as $url) {
            $urlLower = Str::lower($url);

            if (Str::contains($urlLower, 'linkedin.com')) {
                $result['social_media_linkedin'] ??= $url;
            } elseif (Str::contains($urlLower, ['instagram.com', 'instagr.am'])) {
                $result['social_media_instagram'] ??= $url;
            } elseif (Str::contains($urlLower, ['facebook.com', 'fb.com'])) {
                $result['social_media_facebook'] ??= $url;
            } elseif (Str::contains($urlLower, 'tiktok.com')) {
                $result['social_media_tiktok'] ??= $url;
            }
        }

        return $result;
    };

    $dryRun = (bool) $this->option('dry-run');
    $totalRows = 0;
    $importedRows = 0;
    $skippedRows = 0;
    $skipReasons = [
        'invalid_format' => 0,
        'missing_required_fields' => 0,
    ];

    while (($row = fgetcsv($handle, 0, $delimiter)) !== false) {
        if ($row === [null] || $row === []) {
            continue;
        }

        $totalRows++;
        $row = array_pad($row, count($headers), null);
        $assoc = array_combine($headers, $row);

        if (! is_array($assoc)) {
            $skippedRows++;
            $skipReasons['invalid_format']++;
            continue;
        }

        $assoc = array_map(static fn ($value) => is_string($value) ? trim($value) : $value, $assoc);

        $graduationDate = $parseDate($assoc['graduation_date'] ?? null);
        $graduationYear = $graduationDate ? (int) Carbon::parse($graduationDate)->format('Y') : null;

        $socialMedia = $extractSocialMedia($assoc['social_media_bundle'] ?? null);

        $payload = [
            'name' => $assoc['name'] ?: null,
            'nim' => $assoc['nim'] ?: null,
            'entry_year' => is_numeric($assoc['entry_year'] ?? null) ? (int) $assoc['entry_year'] : null,
            'graduation_date' => $graduationDate,
            'faculty' => $assoc['faculty'] ?: null,
            'study_program' => $assoc['study_program'] ?: null,
            'graduation_year' => $graduationYear,
            'email' => $assoc['email'] ?: null,
            'phone_number' => $assoc['phone_number'] ?: null,
            'workplace_name' => $assoc['workplace_name'] ?: null,
            'workplace_address' => $assoc['workplace_address'] ?: null,
            'position' => $assoc['position'] ?: null,
            'employment_type' => $normalizeEmploymentType($assoc['employment_type'] ?? null),
            'workplace_social_media' => $assoc['workplace_social_media'] ?: null,
            'tracking_status' => 'Belum Dilacak',
            ...$socialMedia,
        ];

        if (! $payload['name'] || ! $payload['nim'] || ! $payload['study_program'] || ! $payload['graduation_year']) {
            $skippedRows++;
            $skipReasons['missing_required_fields']++;
            continue;
        }

        if (! $dryRun) {
            Alumni::updateOrCreate(
                ['nim' => $payload['nim']],
                $payload
            );
        }

        $importedRows++;
    }

    fclose($handle);

    $this->info('Import selesai.');
    $this->line("Total baris terbaca: {$totalRows}");
    $this->line("Berhasil diproses: {$importedRows}");
    $this->line("Dilewati: {$skippedRows}");
    $this->line('Rincian dilewati:');
    $this->line('- Format tidak valid: '.$skipReasons['invalid_format']);
    $this->line('- Data wajib kurang: '.$skipReasons['missing_required_fields']);
    $this->line('Mode: '.($dryRun ? 'DRY RUN (tanpa simpan)' : 'SIMPAN DATABASE'));

    return self::SUCCESS;
})->purpose('Import data alumni dari file CSV');
