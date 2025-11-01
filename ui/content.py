"""
HTML content for the Cubyz Addon Manager GUI
"""

INFO_HTML = """
<style>
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #cccccc;
    margin: 0;
    padding: 16px;
    background-color: #1e1e1e;
}
h1, h2, h3 {
    color: #ffffff;
    margin-top: 24px;
    margin-bottom: 12px;
}
h1 {
    font-size: 24px;
    font-weight: 600;
    border-bottom: 2px solid #007acc;
    padding-bottom: 8px;
}
h2 {
    font-size: 18px;
    font-weight: 600;
    margin-top: 28px;
}
h3 {
    font-size: 16px;
    font-weight: 500;
    margin-top: 20px;
}
p {
    margin-bottom: 12px;
}
code {
    background-color: #2d2d30;
    padding: 2px 6px;
    font-family: 'Consolas', 'Courier New', monospace;
    color: #9cdcfe;
    border: 1px solid #3e3e42;
}
ul, ol {
    margin-bottom: 16px;
    padding-left: 20px;
}
li {
    margin-bottom: 6px;
}
.info-box {
    background-color: #252526;
    padding: 12px;
    margin: 16px 0;
    border-left: 3px solid #007acc;
    border: 1px solid #3e3e42;
}
.tip {
    background-color: #252526;
    border-left: 3px solid #28a745;
    border: 1px solid #3e3e42;
}
.warning {
    background-color: #252526;
    border-left: 3px solid #ffc107;
    border: 1px solid #3e3e42;
}
pre {
    background-color: #2d2d30;
    padding: 12px;
    border: 1px solid #3e3e42;
    color: #d4d4d4;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    overflow-x: auto;
}
strong {
    color: #ffffff;
}
</style>

<h1>Cubyz Addon Manager</h1>

<div class="info-box">
    <strong>Welcome!</strong> This tool helps you install and manage addons for Cubyz. 
    Addons extend the game with new blocks, items, biomes, and more.
</div>

<h2>Quick Start</h2>
<p>Place this Executable in the same folder as the Cubyz executable.</p>
<p>Addons are folders placed inside the game's <code>assets</code> directory. They can contain:</p>
<ul>
    <li><code>blocks/</code> — Custom block definitions</li>
    <li><code>items/</code> — New items and tools</li>
    <li><code>biomes/</code> — Environmental biomes</li>
    <li><code>recipes/</code> — Crafting recipes</li>
    <li><code>textures/</code> — Visual assets</li>
</ul>

<h2>Installing from Files</h2>
<div class="tip">
    <strong>Important:</strong> The addon name will be taken from your zip file name, not the folder inside it.
</div>
<ol>
    <li>Click <strong>Install from File...</strong></li>
    <li>Select a <code>.zip</code> file or addon folder</li>
    <li>The addon will be extracted to your assets folder</li>
    <li>If an addon already exists, uninstall it first or use the CLI with <code>--overwrite</code></li>
</ol>

<h2>Installing from GitHub</h2>
<ol>
    <li>Click <strong>Install from URL</strong></li>
    <li>Paste a GitHub repository URL:<br>
        <code>https://github.com/CatchySmile/CubyzAddonManager</code></li>
    <li>The manager will download the latest version automatically</li>
</ol>

<div class="warning">
    <strong>Note:</strong> For private repositories, download the zip manually and use the file installation method.
</div>

<h2>Browse Online Addons</h2>
<p>Use the <strong>Browse</strong> tab to discover and install addons directly from the online repository:</p>
<ol>
    <li>Click the <strong>Browse</strong> tab</li>
    <li>Browse available addons with descriptions and tags</li>
    <li>Click <strong>Install</strong> on any addon you want to add</li>
    <li>Installed addons will show as "Installed" and be grayed out</li>
</ol>

<h2>Creating Your Own Addon</h2>
<p>To create a new addon:</p>
<ol>
    <li>Create a folder with your addon's name</li>
    <li>Add subfolders for the content you want to include</li>
    <li>Create an optional <code>addon.json</code> file with metadata:</li>
</ol>

<pre>{
    "name": "My Awesome Addon",
    "version": "1.0.0",
    "description": "Adds cool new blocks and items",
    "author": "Your Name"
}</pre>

<h2>Safety Features</h2>
<ul>
    <li><strong>Default Assets Protection:</strong> The Cubyz base game assets cannot be removed</li>
    <li><strong>Addon Locking:</strong> All addons start locked to prevent accidental removal</li>
    <li><strong>Unlock Confirmation:</strong> Unlocking an addon requires confirmation</li>
    <li><strong>Removal Confirmation:</strong> Final removal requires additional confirmation</li>
</ul>

<h2>Troubleshooting</h2>
<ul>
    <li><strong>Installation fails:</strong> Check that your zip file is valid and not corrupted</li>
    <li><strong>GitHub download fails:</strong> Ensure the repository is public</li>
    <li><strong>Addon doesn't work:</strong> Check the game logs and verify your JSON files are valid</li>
    <li><strong>Browser shows wrong status:</strong> Click Refresh in the Browse tab</li>
    <li><strong>Need more control:</strong> Use the command-line interface in the CubyzAddonManager folder</li>
</ul>

<div class="info-box">
    <strong>Happy Modding!</strong><br>
    Explore the base game files in <code>assets/cubyz</code> for examples and inspiration.
</div>
"""
