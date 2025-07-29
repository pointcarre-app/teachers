// Load Pyodide
importScripts('https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js');

let pyodide;

async function loadPyodideAndPackages() {
    try {
        pyodide = await self.loadPyodide();

        // // Set up stdout redirection
        // pyodide.setStdout({
        //     write: function(text) {
        //         postMessage({
        //             type: 'stdout',
        //             text: text
        //         });
        //     }
        // });

        await pyodide.loadPackage('micropip');
        await pyodide.runPythonAsync(`
            import micropip
            await micropip.install("sympy")
            # await micropip.install('antlr4-python3-runtime')
            await micropip.install('antlr4-python3-runtime==4.11.1')
        `);
        postMessage({
            type: 'ready',
            message: 'Pyodide loaded and antlr4-python3-runtime installed successfully!'
        });
    } catch (error) {
        postMessage({
            type: 'error',
            message: 'Failed to load Pyodide: ' + error.message
        });
    }
}

// Handle messages from main thread
self.onmessage = async function(e) {
    const { type, code } = e.data;
    
    try {
        switch (type) {
            case 'init':
                await loadPyodideAndPackages();
                break;
                
            case 'run':
                if (!pyodide) {
                    throw new Error('Pyodide not loaded');
                }
                
                const result = await pyodide.runPythonAsync(code);
                postMessage({
                    type: 'result',
                    result: result
                });
                break;
        }
    } catch (error) {
        postMessage({
            type: 'error',
            message: error.message
        });
    }
}; 