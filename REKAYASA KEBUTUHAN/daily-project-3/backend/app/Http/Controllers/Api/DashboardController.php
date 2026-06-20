<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Alumni;
use Illuminate\Http\JsonResponse;

class DashboardController extends Controller
{
    public function index(): JsonResponse
    {
        $total = Alumni::count();
        $teridentifikasi = Alumni::where('tracking_status', 'Teridentifikasi')->count();
        $perluVerifikasi = Alumni::where('tracking_status', 'Perlu Verifikasi')->count();
        $belumDitemukan = Alumni::where('tracking_status', 'Belum Ditemukan')->count();

        return response()->json([
            'total_alumni' => $total,
            'teridentifikasi' => $teridentifikasi,
            'perlu_verifikasi' => $perluVerifikasi,
            'belum_ditemukan' => $belumDitemukan,
            'tracked_alumni' => $teridentifikasi + $perluVerifikasi + $belumDitemukan,
        ]);
    }
}
