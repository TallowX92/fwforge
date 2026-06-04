const vscode = require('vscode');
const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');

function activate(context) {
    let disposable = vscode.commands.registerCommand('fwforge.preview', async (uri) => {
        if (!uri) {
            const editor = vscode.window.activeTextEditor;
            if (editor) uri = editor.document.uri;
            else {
                vscode.window.showErrorMessage('No file selected');
                return;
            }
        }

        const filePath = uri.fsPath;
        const dir = path.dirname(filePath);
        let schemaPath = path.join(dir, 'layout.yaml');
        
        if (!fs.existsSync(schemaPath)) {
            const picked = await vscode.window.showOpenDialog({
                title: 'Select layout.yaml schema file',
                filters: { 'YAML': ['yaml', 'yml'] }
            });
            if (!picked || picked.length === 0) return;
            schemaPath = picked[0].fsPath;
        }

        const cliPath = vscode.workspace.getConfiguration('fwforge').get('cliPath', 'fwforge');
        
        execFile(cliPath, ['-i', filePath, '-s', schemaPath, '-f', 'json'], (err, stdout, stderr) => {
            if (err) {
                vscode.window.showErrorMessage(`CLI error: ${stderr || err.message}\nCheck your layout.yaml and CLI installation.`);
                return;
            }
            
            let data;
            try {
                data = JSON.parse(stdout);
            } catch(e) {
                vscode.window.showErrorMessage('Invalid JSON output from CLI');
                return;
            }

            const panel = vscode.window.createWebviewPanel(
                'fwfPreview',
                `Preview: ${path.basename(filePath)}`,
                vscode.ViewColumn.One,
                { enableScripts: false }
            );
            
            if (data.length === 0) {
                panel.webview.html = "No data found";
                return;
            }

            const columns = Object.keys(data[0]);
            let tableRows = '';
            for (const row of data) {
                tableRows += '<tr>' + columns.map(col => `<td>${escapeHtml(String(row[col] ?? ''))}</td>`).join('') + '</tr>';
            }
            
            panel.webview.html = `<!DOCTYPE html>
            <html>
            <head><style>
                table { border-collapse: collapse; width: 100%; font-family: sans-serif; }
                th, td { border: 1px solid #ccc; padding: 4px 8px; text-align: left; }
                th { background-color: #f0f0f0; position: sticky; top: 0; }
                .container { max-height: 80vh; overflow: auto; }
            </style></head>
            <body>
                <h3>${escapeHtml(path.basename(filePath))}</h3>
                <div class="container">
                    <table>
                        <thead><tr>${columns.map(col => `<th>${escapeHtml(col)}</th>`).join('')}</tr></thead>
                        <tbody>${tableRows}</tbody>
                    </table>
                </div>
                <p><small>Rows: ${data.length} | Schema: ${escapeHtml(path.basename(schemaPath))}</small></p>
            </body>
            </html>`;
        });
    });
    
    context.subscriptions.push(disposable);
}

function escapeHtml(str) {
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

exports.activate = activate;
function deactivate() {}
exports.deactivate = deactivate;
