<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Alumni;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class AlumniController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $search = $request->query('search');
        $perPage = (int) $request->query('per_page', 10);

        $alumni = Alumni::query()
            ->when($search, function ($query, $searchTerm) {
                $query->where('name', 'like', "%{$searchTerm}%")
                    ->orWhere('nim', 'like', "%{$searchTerm}%")
                    ->orWhere('study_program', 'like', "%{$searchTerm}%")
                    ->orWhere('email', 'like', "%{$searchTerm}%");
            })
            ->latest()
            ->paginate($perPage);

        return response()->json($alumni);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'nim' => ['required', 'string', 'max:100', 'unique:alumni,nim'],
            'study_program' => ['required', 'string', 'max:255'],
            'graduation_year' => ['required', 'integer', 'digits:4', 'min:1900'],
            'email' => ['nullable', 'email', 'max:255'],
        ]);

        $alumni = Alumni::create($validated);

        return response()->json($alumni, 201);
    }

    public function show(Alumni $alumni): JsonResponse
    {
        $alumni->load('trackingResults');

        return response()->json($alumni);
    }

    public function update(Request $request, Alumni $alumni): JsonResponse
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'nim' => ['required', 'string', 'max:100', 'unique:alumni,nim,'.$alumni->id],
            'study_program' => ['required', 'string', 'max:255'],
            'graduation_year' => ['required', 'integer', 'digits:4', 'min:1900'],
            'email' => ['nullable', 'email', 'max:255'],
            'tracking_status' => ['nullable', 'in:Belum Dilacak,Teridentifikasi,Perlu Verifikasi,Belum Ditemukan'],
        ]);

        $alumni->update($validated);

        return response()->json($alumni->fresh());
    }

    public function destroy(Alumni $alumni): JsonResponse
    {
        $alumni->delete();

        return response()->json([
            'message' => 'Data alumni berhasil dihapus.',
        ]);
    }
}
