import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.jsx',
            publicDirectory: '../backend/public',
            hotFile: '../backend/public/hot',
            buildDirectory: 'build',
            refresh: [
                '../backend/app/**',
                '../backend/routes/**',
                '../backend/resources/views/**',
            ],
        }),
        react(),
    ],
});
