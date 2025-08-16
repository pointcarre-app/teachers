import { Nagini } from "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js";

// ===== Configuration for antlr4/micropip test (minimal manager) =====
// Create minimal manager just for testing micropip installation
console.log("📦 Creating minimal Nagini manager for micropip test...");

// Load the antlr4 test file and tests/__init__.py
const antlr4TestFiles = [
    {
        url: `${window.location.origin}/tests/__init__.py`,
        path: "tests/__init__.py"
    },
    {
        url: `${window.location.origin}/tests/test_antlr4.py`,
        path: "tests/test_antlr4.py"
    }
];

const micropipPackagesAntlr4 = ["antlr4-python3-runtime==4.11.0"];
const antlr4Manager = await Nagini.createManager(
    'pyodide',
    [], // No regular packages needed
    micropipPackagesAntlr4, // Test micropip installation
    antlr4TestFiles, // Load the test files
    'https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js'
);

await Nagini.waitForReady(antlr4Manager);
console.log("✅ micropip test manager is ready.");

// ===== Configuration for unit tests (separate manager) =====
const backend = "pyodide";
const packages = ["sympy", "pydantic"];  // Regular packages for unit tests
const micropipPackages = [];  // No micropip packages needed for unit tests
const workerUrl = "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js";

const sourceFiles = [
    "src/teachers/__init__.py",
    "src/teachers/corrector.py",
    "src/teachers/defaults.py",
    "src/teachers/formatting.py",
    "src/teachers/generator.py",
    "src/teachers/maths.py"
];

const testFiles = [
    "tests/test_add_simplification.py",
    "tests/test_mul_simplification.py",
    "tests/test_as_decimal.py",
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
    "tests/test_maths_collection_sympy.py",
    "tests/test_negative_exponents.py"
];

// Detect if we're running on GitHub Pages or localhost
const isGitHubPages = window.location.hostname.includes('github.io');
// Use the actual origin to avoid CORS issues between localhost and 127.0.0.1
const baseUrl = isGitHubPages ? window.location.origin + '/teachers/' : window.location.origin + '/';

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

// Create manager for unit tests
console.log("📦 Creating Nagini manager for unit tests...");
const manager = await Nagini.createManager(
  backend,                  // 'pyodide'
  packages,                 // ['sympy', 'pydantic'] - Regular packages
  micropipPackages,         // [] - No micropip packages for unit tests
  filesToLoad,              // Teachers module files and test files
  workerUrl                 // Nagini v0.0.21 worker URL
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

    // Get test description based on filename
    const getTestDescription = (fileName) => {
        const descriptions = {
            'test_complex_operations.py': 'Complex mathematical operations and interactions',
            'test_deserialization_from_formal.py': 'Formal representation parsing and deserialization',
            'test_deserialization_from_sympy.py': 'SymPy expression conversion and integration',
            'test_generator.py': 'Mathematical content generation utilities',
            'test_maths_objects.py': 'Core mathematical object creation and validation',
            'test_latex_output.py': 'LaTeX generation and formatting',
            'test_interval.py': 'Mathematical intervals and set operations',
            'test_corrector.py': 'Student response correction and feedback',
            'test_formatting.py': 'Educational formatting standards (French)',
            'test_eval_methods.py': 'Numerical evaluation and computation',
            'test_inf.py': 'Infinity handling and mathematical limits',
            'test_maths_collection_sympy.py': 'Mathematical collections and SymPy integration'
        };
        return descriptions[fileName] || 'Mathematical framework functionality';
    };

    const description = getTestDescription(testFileName);
    const row = document.createElement("tr");
    row.id = rowId;
    row.innerHTML = `
        <td style="text-align: right;vertical-align: top;">${index + 8}️⃣</td>
        <td style="text-align: left;vertical-align: top;"><code>${testFileName}</code></td>
        <td style="text-align: left;vertical-align: top;"><code>teachers</code><br/>${description}</td>
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
    try {
    const executionResult = await manager.executeAsync(`${moduleName}_runner.py`, testRunnerCode);
        console.log(`Test ${testFileName} execution result:`, executionResult);

    // Update logs
    const outputElement = document.getElementById("output");
    let missive = executionResult.missive;

    if(outputElement) {
        const currentOutput = outputElement.textContent;
            const formattedMessage = JSON.stringify(executionResult, null, 2);
        outputElement.textContent = currentOutput + "\n" + formattedMessage;
        updateSummaryLineCount("logs-summary", outputElement.textContent, "Display JS logs");
    }

        if (!executionResult) {
            updateTestResult({
                testFile: testFileName,
                status: 'fail',
                summary: 'No result from test execution'
            });
            return;
        }

        if (executionResult.error) {
            updateTestResult({
                testFile: testFileName,
                status: 'fail',
                summary: `Execution error: ${executionResult.error}`
            });
            return;
    }

    if (typeof missive === 'string') {
        try {
            missive = JSON.parse(missive);
        } catch (e) {
            console.error("Failed to parse missive from worker:", missive);
            updateTestResult({
                testFile: testFileName,
                status: 'fail',
                    summary: `Failed to parse results from test script: ${e.message}\nRaw output: ${missive}`
            });
            return;
        }
    }

        if (missive && missive.type === 'test_result') {
        updateTestResult(missive.payload);
    } else {
        // Handle cases where the test script fails to produce a missive
            updateTestResult({
                testFile: testFileName,
                status: 'fail',
                summary: `Test did not produce expected result format. Output: ${executionResult.output || 'No output'}`
            });
        }
    } catch (error) {
        console.error(`Error running test ${testFileName}:`, error);
        updateTestResult({
            testFile: testFileName,
            status: 'fail',
            summary: `Exception during test execution: ${error.message}`
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


// Wait for unit test manager
await Nagini.waitForReady(manager);
console.log("✅ Unit test manager is ready.");

// Test 1: Check if micropip can install antlr4-python3-runtime
console.log("🔍 Testing micropip installation of antlr4-python3-runtime...");

// Run the antlr4 test using unittest like other tests
const antlr4TestRunnerCode = `
import unittest
import sys
import json

# Run the antlr4 import test
loader = unittest.TestLoader()
suite = loader.loadTestsFromName('tests.test_antlr4')
runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
result = runner.run(suite)

# Report results
if result.wasSuccessful():
    print("\\n✅ All antlr4 tests passed")
    missive({
        "status": "pass",
        "total": result.testsRun,
        "passed": result.testsRun,
        "failed": 0
    })
else:
    print(f"\\n❌ {len(result.failures)} test(s) failed")
    missive({
        "status": "fail",
        "total": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures) + len(result.errors)
    })
`;

try {
    const result = await antlr4Manager.executeAsync("run_antlr4_test.py", antlr4TestRunnerCode);
    
    if (result.stdout) {
        console.log("📝 antlr4 test output:\n", result.stdout);
    }
    if (result.stderr) {
        console.error("⚠️ antlr4 test stderr:\n", result.stderr);
    }
    
    // Parse missive if it's a string
    let missive = result.missive;
    if (typeof missive === 'string') {
        try {
            missive = JSON.parse(missive);
        } catch (e) {
            console.error("Failed to parse missive:", e);
        }
    }
    
    const statusCell = document.getElementById('status-nagini-1');
    if (statusCell) {
        if (result && missive && missive.status === 'pass') {
            statusCell.className = 'test-status-pass';
            statusCell.textContent = '✅';
            console.log("✅ antlr4 tests PASSED! Results:", missive);
        } else {
            statusCell.className = 'test-status-fail';
            statusCell.textContent = '❌';
            console.error("❌ antlr4 tests failed:", missive);
        }
    }
} catch (error) {
    console.error("❌ Error running antlr4 test:", error);
    const statusCell = document.getElementById('status-nagini-1');
    if (statusCell) {
        statusCell.className = 'test-status-fail';
        statusCell.textContent = '❌';
    }
}

// Run quick validation tests for negative exponents
const negativeExponentTestCode = `
import unittest
import sys
import json

# Quick validation that the fix is working
try:
    import teachers.maths as tm
    import teachers.generator as tg
    
    results = []
    
    # Test 1: Basic negative exponents
    try:
        # This is what was failing before
        b = tm.Integer(n=10) ** tm.Integer(n=-2)
        b_simplified = b.simplified()
        if hasattr(b_simplified, 'as_decimal'):
            b_decimal = b_simplified.as_decimal
            results.append({"id": "status-teachers-negative-exp", "status": "pass"})
        else:
            results.append({"id": "status-teachers-negative-exp", "status": "fail", "error": "No as_decimal method"})
    except Exception as e:
        results.append({"id": "status-teachers-negative-exp", "status": "fail", "error": str(e)})
    
    # Test 2: Decimal conversion
    try:
        val = tm.Integer(n=10) ** tm.Integer(n=-3)
        val_simplified = val.simplified()
        val_decimal = val_simplified.as_decimal
        if abs(val_decimal.eval() - 0.001) < 1e-10:
            results.append({"id": "status-teachers-decimal-conv", "status": "pass"})
        else:
            results.append({"id": "status-teachers-decimal-conv", "status": "fail", "error": "Wrong value"})
    except Exception as e:
        results.append({"id": "status-teachers-decimal-conv", "status": "fail", "error": str(e)})
    
    # Test 3: Add simplification (Integer + Decimal, Decimal + Fraction)
    try:
        # Test Integer + Decimal
        integer = tm.Integer(n=5)
        decimal = tm.Decimal(p=1, q=4)  # 0.25
        add_expr = integer + decimal
        simplified = add_expr.simplified()
        if isinstance(simplified, tm.Decimal) and simplified.x == 5.25:
            # Test Decimal + Fraction
            decimal2 = tm.Decimal(p=1, q=4)  # 0.25
            fraction = tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=2))  # 0.5
            add_expr2 = decimal2 + fraction
            simplified2 = add_expr2.simplified()
            if isinstance(simplified2, tm.Decimal) and simplified2.x == 0.75:
                results.append({"id": "status-teachers-add-simplification", "status": "pass"})
            else:
                results.append({"id": "status-teachers-add-simplification", "status": "fail", "error": "Decimal+Fraction failed"})
        else:
            results.append({"id": "status-teachers-add-simplification", "status": "fail", "error": "Integer+Decimal failed"})
    except Exception as e:
        results.append({"id": "status-teachers-add-simplification", "status": "fail", "error": str(e)})
    
    # Test 4: Mul simplification (Integer * Mul nested operations)
    try:
        # Test Integer * Mul(Integer, Symbol) - reproduces user's error
        x = tm.Symbol(s="x")
        inner_mul = tm.Mul(l=tm.Integer(n=3), r=x)  # 3x
        outer_mul = tm.Mul(l=tm.Integer(n=2), r=inner_mul)  # 2 * (3x)
        simplified = outer_mul.simplified()
        
        # Should simplify to 6x
        expected = tm.Mul(l=tm.Integer(n=6), r=x)
        if simplified == expected:
            # Test polynomial expansion scenario: (3x + 4)^2
            a = tm.Integer(n=3)
            b = tm.Integer(n=4)
            polynomial = tm.Pow(base=tm.Add(l=tm.Mul(l=a, r=x), r=b), exp=tm.Integer(n=2))
            expanded = polynomial.simplified()
            # Should not raise NotImplementedError and should be an Add expression
            if isinstance(expanded, tm.Add):
                results.append({"id": "status-teachers-mul-simplification", "status": "pass"})
            else:
                results.append({"id": "status-teachers-mul-simplification", "status": "fail", "error": "Polynomial expansion failed"})
        else:
            results.append({"id": "status-teachers-mul-simplification", "status": "fail", "error": "Integer*Mul failed"})
    except Exception as e:
        results.append({"id": "status-teachers-mul-simplification", "status": "fail", "error": str(e)})
    
    # Test 5: as_decimal property (Integer.as_decimal and clean Decimal.latex())
    try:
        # Test Integer.as_decimal property
        integer = tm.Integer(n=5)
        decimal_result = integer.as_decimal
        if isinstance(decimal_result, tm.Decimal):
            # Test clean LaTeX output for whole numbers (no decimal point)
            latex_output = decimal_result.latex()
            if latex_output == "5":  # Should be "5", not "5.0" or "5,0"
                # Test fractional decimal LaTeX (should use period, not comma)
                frac_decimal = tm.Decimal(x=3.25)
                frac_latex = frac_decimal.latex()
                if frac_latex == "3.25" and "," not in frac_latex:
                    # Test the original user scenario: (p * n1).simplified().as_decimal
                    p = tm.Fraction(p=tm.Integer(n=146), q=tm.Integer(n=10))  # 14.6
                    n1 = tm.Integer(n=3)
                    user_result = (p * n1).simplified()
                    user_decimal = user_result.as_decimal  # This was failing before
                    if hasattr(user_result, 'as_decimal') and isinstance(user_decimal, tm.Decimal):
                        results.append({"id": "status-teachers-as-decimal", "status": "pass"})
                    else:
                        results.append({"id": "status-teachers-as-decimal", "status": "fail", "error": "User scenario failed"})
                else:
                    results.append({"id": "status-teachers-as-decimal", "status": "fail", "error": "Fractional LaTeX failed"})
            else:
                results.append({"id": "status-teachers-as-decimal", "status": "fail", "error": "Whole number LaTeX failed"})
        else:
            results.append({"id": "status-teachers-as-decimal", "status": "fail", "error": "as_decimal not Decimal type"})
    except Exception as e:
        results.append({"id": "status-teachers-as-decimal", "status": "fail", "error": str(e)})
    
    # Test 6: Original scenario
    try:
        gen = tg.MathsGenerator(0)
        n1 = gen.random_integer(1, 4)
        n2 = gen.random_integer(1, 4)
        n3 = gen.random_integer(1, 4)
        
        a = tm.Integer(n=10) ** n1
        b = tm.Integer(n=10) ** (-n2)
        c = tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=10) ** n3)
        
        b_simplified = b.simplified().as_decimal
        c_simplified = c.simplified()
        
        expr = a + b_simplified + c_simplified
        results.append({"id": "status-teachers-original-bug", "status": "pass"})
    except Exception as e:
        results.append({"id": "status-teachers-original-bug", "status": "fail", "error": str(e)})
    
    # Send results
    missive({"type": "batch_update", "results": results})
    
except Exception as e:
    # If imports fail, mark all as failed
    error_msg = str(e)
    missive({"type": "batch_update", "results": [
        {"id": "status-teachers-negative-exp", "status": "fail", "error": error_msg},
        {"id": "status-teachers-decimal-conv", "status": "fail", "error": error_msg},
        {"id": "status-teachers-add-simplification", "status": "fail", "error": error_msg},
        {"id": "status-teachers-mul-simplification", "status": "fail", "error": error_msg},
        {"id": "status-teachers-as-decimal", "status": "fail", "error": error_msg},
        {"id": "status-teachers-original-bug", "status": "fail", "error": error_msg}
    ]})
`;

try {
    const negExpResult = await manager.executeAsync("negative_exp_test.py", negativeExponentTestCode);
    console.log("Negative exponent test result:", negExpResult);
    
    if (negExpResult && negExpResult.stderr) {
        console.error("Negative exponent test stderr:", negExpResult.stderr);
    }
    
    if (negExpResult && negExpResult.missive) {
        let msg;
        try {
            msg = typeof negExpResult.missive === 'string' ? JSON.parse(negExpResult.missive) : negExpResult.missive;
        } catch (e) {
            console.error("Failed to parse missive:", e);
            msg = null;
        }
        
        if (msg && msg.type === 'batch_update' && msg.results) {
            msg.results.forEach(update => {
                const statusCell = document.getElementById(update.id);
                if (statusCell) {
                    if (update.status === 'pass') {
                        statusCell.className = 'test-status-pass';
                        statusCell.textContent = '✅';
                    } else {
                        statusCell.className = 'test-status-fail';
                        statusCell.textContent = '❌';
                        console.error(`Test ${update.id} failed:`, update.error);
                    }
                }
            });
        }
    } else {
        // If tests failed to run, mark them as failed
        ['status-teachers-negative-exp', 'status-teachers-decimal-conv', 'status-teachers-add-simplification', 'status-teachers-mul-simplification', 'status-teachers-as-decimal', 'status-teachers-original-bug'].forEach(id => {
            const statusCell = document.getElementById(id);
            if (statusCell) {
                statusCell.className = 'test-status-fail';
                statusCell.textContent = '❌';
            }
        });
        console.error("Failed to run negative exponent tests - no missive");
    }
} catch (error) {
    console.error("Error running negative exponent tests:", error);
    ['status-teachers-negative-exp', 'status-teachers-decimal-conv', 'status-teachers-add-simplification', 'status-teachers-mul-simplification', 'status-teachers-as-decimal', 'status-teachers-original-bug'].forEach(id => {
        const statusCell = document.getElementById(id);
        if (statusCell) {
            statusCell.className = 'test-status-fail';
            statusCell.textContent = '❌';
        }
    });
}

// Run all individual test files (but exclude duplicates that are already in Unit Tests)
console.log("Running individual test files...");
const individualTests = testFiles.filter(testFile => {
    // Exclude tests that are already covered in the Unit Tests section above
    const excludedTests = [
        'tests/test_negative_exponents.py',
        'tests/test_add_simplification.py', 
        'tests/test_mul_simplification.py',
        'tests/test_as_decimal.py'
    ];
    return !excludedTests.includes(testFile);
});

for (const [index, testFile] of individualTests.entries()) {
    console.log(`Running individual test ${index + 1}/${individualTests.length}: ${testFile}`);
    await runTest(testFile, index);
}
console.log("All tests completed.");
