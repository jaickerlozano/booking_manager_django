/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        /**
         * Archivos de Django y Python donde usarás las clases.
         */
        '../../core/templates/**/*.html',
        
        /**
         * ¡Ruta crucial para que Tailwind escanee los componentes de Flowbite!
         */
        './node_modules/flowbite/**/*.js'
    ],
    theme: {
        extend: {
            // Aquí defines tu paleta personalizada
            colors: {
                'brand-blue': '#1e3a8a',
                'brand-emerald': '#10b981',
            }
        },
    },
    plugins: [
        /**
         * Plugins requeridos por Django-Tailwind y Flowbite
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('flowbite/plugin') // Carga de Flowbite
    ],
}
