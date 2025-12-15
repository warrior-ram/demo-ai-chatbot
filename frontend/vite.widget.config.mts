import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            "@": resolve(__dirname, "./"),
        },
    },
    build: {
        outDir: 'public',
        emptyOutDir: false,
        lib: {
            entry: resolve(__dirname, 'widget/index.tsx'),
            name: 'ChatWidget',
            fileName: () => 'embed.js',
            formats: ['iife'],
        },
        rollupOptions: {
            external: [],
            output: {
                globals: {},
            },
        },
        minify: true,
    },
    define: {
        'process.env.NODE_ENV': '"production"',
    },
});
