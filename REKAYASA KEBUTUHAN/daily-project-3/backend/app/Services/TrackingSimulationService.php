<?php

namespace App\Services;

use App\Models\Alumni;

class TrackingSimulationService
{
    /**
     * @return array{queries: array<int, string>, candidates: array<int, array<string, mixed>>}
     */
    public function simulate(Alumni $alumni): array
    {
        $queries = $this->buildQueries($alumni);

        return [
            'queries' => $queries,
            'candidates' => $this->generateCandidates($alumni, $queries),
        ];
    }

    /**
     * @return array<int, string>
     */
    private function buildQueries(Alumni $alumni): array
    {
        $university = 'Universitas';
        $location = 'Indonesia';

        return [
            sprintf('"%s" %s alumni %s', $alumni->name, $alumni->study_program, $university),
            sprintf('"%s" %s %s', $alumni->name, $alumni->study_program, $location),
            sprintf('"%s" NIM %s', $alumni->name, $alumni->nim),
            sprintf('"%s" career profile %s', $alumni->name, $location),
        ];
    }

    /**
     * @param array<int, string> $queries
     * @return array<int, array<string, mixed>>
     */
    private function generateCandidates(Alumni $alumni, array $queries): array
    {
        $baseSeed = crc32($alumni->nim.$alumni->name);
        mt_srand($baseSeed);

        $sources = [
            ['Google Search', 'https://www.google.com/search?q='],
            ['Professional Platform', 'https://www.linkedin.com/in/'],
            ['Institution Website', 'https://alumni.university.example/profile/'],
            ['News Website', 'https://news.example.com/search?q='],
        ];

        $candidates = [];

        foreach ($sources as $index => [$source, $baseUrl]) {
            $query = $queries[$index % count($queries)];
            $score = mt_rand(55, 95) + (mt_rand(0, 99) / 100);
            $slug = strtolower(str_replace(' ', '-', preg_replace('/[^A-Za-z0-9 ]/', '', $alumni->name)));

            $candidates[] = [
                'source' => $source,
                'title' => sprintf('%s - %s Alumni Profile', $alumni->name, $alumni->study_program),
                'description' => sprintf(
                    'Simulation result from %s using query: %s. Indicates possible current activity related to %s.',
                    $source,
                    $query,
                    $alumni->study_program
                ),
                'url' => $source === 'Professional Platform'
                    ? $baseUrl.$slug
                    : $baseUrl.urlencode($query),
                'confidence_score' => round($score, 2),
                'status' => 'Perlu Verifikasi',
            ];
        }

        usort(
            $candidates,
            fn (array $a, array $b): int => $b['confidence_score'] <=> $a['confidence_score']
        );

        return $candidates;
    }
}
