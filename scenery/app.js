import { Nagini } from "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@0.0.5/src/nagini.js";

const backend = "pyodide";
const packages = ["sympy", "pydantic"];
const micropipPackages = ["antlr4-python3-runtime==4.11.0"];
const workerUrl = "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@0.0.5/src/pyodide/worker/worker-dist.js";

const sourceFiles = [
    "src/teachers/__init__.py",
    "src/teachers/corrector.py",
    "src/teachers/defaults.py",
    "src/teachers/formatting.py",
    "src/teachers/generator.py",
    "src/teachers/maths.py"
];

const testFiles = [
    "tests/test_complex_operations.py",
    "tests/test_deserialization_from_formal.py",
    "tests/test_deserialization_from_sympy.py",
    "tests/test_generator.py",
    "tests/test_maths_objects.py",
    "tests/test_latex_output.py",
    "tests/test_interval.py",
    "tests/test_corrector.py",
    "tests/test_formatting.py",
    "tests/test_eval_methods.py",
    "tests/test_inf.py",
    "tests/test_maths_collection_sympy.py"
];

// Detect if we're running on GitHub Pages or localhost
const isGitHubPages = window.location.hostname.includes('github.io');
const baseUrl = isGitHubPages ? window.location.origin + window.location.pathname : 'http://127.0.0.1:8001';

const filesToLoad = [...sourceFiles, ...testFiles].map(file => {
    const path = file.startsWith('src/') ? file.substring(4) : file;
    return {
        url: `${baseUrl}${file}`,
        path: path
    };
});

// also need to load __init__.py and __main__.py from tests
filesToLoad.push({url: `${baseUrl}tests/__init__.py`, path: `tests/__init__.py`});
filesToLoad.push({url: `${baseUrl}tests/__main__.py`, path: `tests/__main__.py`});


const manager = await Nagini.createManager(
  backend,
  packages,
  micropipPackages,
  filesToLoad,
  workerUrl
);

function updateSummaryLineCount(summaryId, content, baseText) {
    const summaryElement = document.getElementById(summaryId);
    if (summaryElement) {
        const lineCount = content ? content.split('\n').length : 0;
        summaryElement.textContent = `${baseText} [Lines from logs: ${lineCount}]`;
    }
};

async function runTest(testFile, index) {
    const testFileName = testFile.split('/').pop();
    const moduleName = testFileName.replace('.py', '');
    
    // Add a placeholder row
    const tbody = document.getElementById("tests-body");
    const rowId = `test-row-${moduleName}`;
    const statusId = `status-${moduleName}`;
    const summaryId = `summary-${moduleName}`;
    const detailsId = `details-${moduleName}`;

    const row = document.createElement("tr");
    row.id = rowId;
    row.innerHTML = `
        <td style="text-align: right;vertical-align: top;">${index + 2}️⃣</td>
        <td style="text-align: left;vertical-align: top;"><code>teachers</code></td>
        <td style="text-align: left;vertical-align: top;">${testFileName}</td>
        <td id="${statusId}" class="test-status-pending">⏳</td>
    `;
    tbody.appendChild(row);

    const testRunnerCode = `
import unittest
import io
import sys
import json

# The test module to run
test_module_name = '${moduleName}'

# Import the test module
try:
    __import__('tests.' + test_module_name)
except ImportError as e:
    # Send error message back
    missive({
        "type": "test_result", 
        "payload": {
            "testFile": "${testFileName}",
            "status": "fail",
            "summary": f"Failed to import module: {e}"
        }
    })
else:
    # Discover and run tests in the specific module
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName('tests.' + test_module_name)
    
    output = io.StringIO()
    runner = unittest.TextTestRunner(stream=output, verbosity=2)
    result = runner.run(suite)

    summary_text = output.getvalue()

    status = 'pass' if result.wasSuccessful() else 'fail'

    # Send results back
    missive({
        "type": "test_result",
        "payload": {
            "testFile": "${testFileName}",
            "status": status,
            "summary": summary_text,
            "passed": result.testsRun - len(result.failures) - len(result.errors),
            "total": result.testsRun
        }
    })
`;
    const executionResult = await manager.executeAsync(`${moduleName}_runner.py`, testRunnerCode);

    // Update logs
    const outputElement = document.getElementById("output");
    let missive = executionResult.missive;

    if(outputElement) {
        const currentOutput = outputElement.textContent;
        const formattedMessage = JSON.stringify(missive, null, 2);
        outputElement.textContent = currentOutput + "\n" + formattedMessage;
        updateSummaryLineCount("logs-summary", outputElement.textContent, "Display JS logs");
    }

    if (typeof missive === 'string') {
        try {
            missive = JSON.parse(missive);
        } catch (e) {
            console.error("Failed to parse missive from worker:", missive);
            updateTestResult({
                testFile: testFileName,
                status: 'fail',
                summary: `Failed to parse results from test script: ${e.message}`
            });
            return;
        }
    }

    if (executionResult && missive && missive.type === 'test_result') {
        updateTestResult(missive.payload);
    } else {
        // Handle cases where the test script fails to produce a missive
        updateTestResult({
            testFile: testFileName,
            status: 'fail',
            summary: `Execution failed. Error: ${executionResult.error || 'Unknown error'}`
        });
    }
}

function updateTestResult(result) {
    const moduleName = result.testFile.replace('.py', '');
    const statusCell = document.getElementById(`status-${moduleName}`);
    const testRow = document.getElementById(`test-row-${moduleName}`);

    if (!statusCell || !testRow) {
        console.error(`Could not find DOM elements for ${moduleName} to update test results.`);
        return;
    }

    if (result.status === 'pass') {
        statusCell.className = 'test-status-pass';
        statusCell.textContent = '✅';
    } else {
        statusCell.className = 'test-status-fail';
        statusCell.textContent = '❌';
    }

    const summaryRow = document.createElement('tr');
    summaryRow.className = 'summary-row';

    let summaryText = '';
    if (result.status === 'pass') {
        summaryText = `All ${result.total} tests passed!`;
    } else {
        if (result.total > 0) {
           summaryText = `${result.passed} / ${result.total} passed.`;
        } else {
           summaryText = `Test execution failed.`;
        }
    }
    
    summaryRow.innerHTML = `
        <td colspan="4">
            <b>${summaryText}</b>
            <details>
                <summary>Click for full logs</summary>
                <pre>${result.summary}</pre>
            </details>
        </td>
    `;
    testRow.parentNode.insertBefore(summaryRow, testRow.nextSibling);
}


await Nagini.waitForReady(manager);
console.log("Manager is ready.");

for (const [index, testFile] of testFiles.entries()) {
    await runTest(testFile, index);
}
