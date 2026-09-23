from flask import Flask, render_template_string, jsonify
from datetime import datetime
import os

# Specify your actual GitHub repository URL here
GITHUB_REPO_URL = "https://github.com/your-username/your-repo-name"

application = Flask(__name__)

# HTML template styled as a colourful telecom "network coverage" dashboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SLT Mobitel | AWS Cloud Hosting — Deployment Status</title>
    <script>
        function updateClock() {
            const now = new Date();
            const el = document.getElementById('server-time');
            if (el) el.textContent = now.toISOString().replace('T', ' ').substr(0, 19) + ' UTC';
        }
        setInterval(updateClock, 1000);
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap');

        :root {
            --navy-950: #0A1128;
            --navy-900: #10193A;
            --navy-800: #182653;
            --line: rgba(148, 163, 196, 0.16);
            --text-primary: #F4F6FB;
            --text-muted: #8C9AC0;
            --green: #7DC242;
            --orange: #F7941D;
            --blue: #00AEEF;
            --magenta: #EC1E79;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: 'IBM Plex Sans', sans-serif;
            background-color: var(--navy-950);
            background-image:
                repeating-linear-gradient(115deg, rgba(0,174,239,0.05) 0px, rgba(0,174,239,0.05) 1px, transparent 1px, transparent 90px),
                repeating-linear-gradient(25deg, rgba(125,194,66,0.04) 0px, rgba(125,194,66,0.04) 1px, transparent 1px, transparent 90px);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .mono { font-family: 'IBM Plex Mono', monospace; }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 32px;
            border-bottom: 1px solid var(--line);
            max-width: 1180px;
            width: 100%;
            margin: 0 auto;
        }

        .brand { display: flex; align-items: center; gap: 14px; }

        .signal-mark { position: relative; width: 26px; height: 26px; flex-shrink: 0; }
        .signal-mark .dot {
            position: absolute; inset: 0; margin: auto;
            width: 8px; height: 8px; border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 10px var(--green);
        }
        .signal-mark .ring {
            position: absolute; inset: 0; margin: auto;
            border-radius: 50%; border: 1.5px solid;
            width: 8px; height: 8px; opacity: 0;
            animation: pulseRing 2.8s ease-out infinite;
        }
        .signal-mark .ring:nth-child(2) { border-color: var(--orange); animation-delay: 0.5s; }
        .signal-mark .ring:nth-child(3) { border-color: var(--blue); animation-delay: 1s; }
        .signal-mark .ring:nth-child(4) { border-color: var(--magenta); animation-delay: 1.5s; }
        @keyframes pulseRing {
            0%   { width: 8px; height: 8px; opacity: 0.9; }
            100% { width: 30px; height: 30px; opacity: 0; }
        }

        .wordmark { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1rem; letter-spacing: 0.02em; }
        .wordmark span { color: var(--orange); }
        .tagline { font-size: 0.7rem; color: var(--text-muted); letter-spacing: 0.08em; margin-top: 1px; }

        .region-chip {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            color: var(--blue);
            border: 1px solid rgba(0,174,239,0.35);
            background: rgba(0,174,239,0.08);
            padding: 6px 12px;
            border-radius: 3px;
        }

        main {
            flex-grow: 1;
            max-width: 1180px;
            width: 100%;
            margin: 0 auto;
            padding: 48px 32px;
        }

        .grid {
            display: grid;
            grid-template-columns: 1.7fr 1fr;
            gap: 24px;
        }

        .panel {
            background: linear-gradient(180deg, var(--navy-900), var(--navy-800));
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 32px;
        }

        .hero-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }

        h1 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: clamp(1.9rem, 4vw, 2.7rem);
            font-weight: 700;
            line-height: 1.1;
            margin: 0 0 8px 0;
        }

        .status-live {
            display: inline-flex; align-items: center; gap: 8px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.85rem;
            color: var(--green);
            border: 1px solid rgba(125,194,66,0.4);
            background: rgba(125,194,66,0.08);
            padding: 8px 14px;
            border-radius: 3px;
            white-space: nowrap;
        }
        .status-live .blip { width: 7px; height: 7px; border-radius: 50%; background: var(--green); box-shadow: 0 0 8px var(--green); }

        .hero-desc { color: var(--text-muted); font-size: 0.98rem; line-height: 1.7; max-width: 46ch; margin-top: 18px; }
        .hero-desc strong { color: var(--text-primary); font-weight: 500; }

        .log {
            margin-top: 28px;
            background: rgba(0,0,0,0.35);
            border: 1px solid var(--line);
            border-radius: 5px;
            padding: 18px 20px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.78rem;
            line-height: 1.9;
        }
        .log .row { display: flex; gap: 10px; color: var(--text-muted); }
        .log .ok { color: var(--green); }
        .log .arrow { color: var(--blue); }

        .stats { display: flex; flex-direction: column; gap: 14px; }

        .stat-card {
            background: var(--navy-900);
            border: 1px solid var(--line);
            border-left: 3px solid var(--accent, var(--blue));
            border-radius: 4px;
            padding: 16px 18px;
        }
        .stat-card .label { font-size: 0.7rem; color: var(--text-muted); letter-spacing: 0.06em; }
        .stat-card .value { font-family: 'IBM Plex Mono', monospace; font-size: 1.15rem; margin-top: 5px; font-weight: 500; }

        .actions { margin-top: 20px; display: flex; flex-direction: column; gap: 10px; }

        .btn {
            display: block; text-align: center;
            padding: 13px 18px;
            border-radius: 4px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            font-size: 0.88rem;
            text-decoration: none;
            transition: opacity 0.15s ease;
        }
        .btn:hover { opacity: 0.85; }
        .btn-primary { background: var(--green); color: var(--navy-950); }
        .btn-outline { border: 1px solid rgba(0,174,239,0.45); color: var(--blue); display: flex; align-items: center; justify-content: center; gap: 8px; }

        footer {
            border-top: 2px solid transparent;
            border-image: linear-gradient(90deg, var(--green), var(--orange), var(--blue), var(--magenta)) 1;
            text-align: center;
            padding: 18px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            color: var(--text-muted);
        }

        @media (max-width: 800px) {
            .grid { grid-template-columns: 1fr; }
            header { flex-direction: column; align-items: flex-start; gap: 12px; }
        }
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <div class="signal-mark">
                <span class="ring"></span><span class="ring"></span><span class="ring"></span>
                <span class="dot"></span>
            </div>
            <div>
                <div class="wordmark">SLT <span>MOBITEL</span> CLOUD</div>
                <div class="tagline">AWS WEB HOSTING NODE</div>
            </div>
        </div>
        <div class="region-chip">REGION: {{ aws_region }}</div>
    </header>

    <main>
        <div class="grid">

            <div class="panel">
                <div class="hero-top">
                    <h1>Deployment is live and serving traffic.</h1>
                    <span class="status-live"><span class="blip"></span>ACTIVE</span>
                </div>
                <p class="hero-desc">
                    This AWS Elastic Beanstalk environment finished provisioning and passed its health checks.
                    The app is running on a <strong>Python / Gunicorn</strong> runtime behind Flask, deployed for
                    <strong>{{ env_name }}</strong>.
                </p>

                <div class="log">
                    <div class="row"><span class="arrow">&gt;</span> initializing elastic beanstalk deployment <span class="ok">[ok]</span></div>
                    <div class="row"><span class="arrow">&gt;</span> verifying requirements.txt <span class="ok">[ok]</span></div>
                    <div class="row"><span class="arrow">&gt;</span> starting gunicorn worker processes <span class="ok">[ok]</span></div>
                    <div class="row"><span class="arrow">&gt;</span> application health check <span class="ok">[ok]</span></div>
                    <div class="row" style="color: var(--green);"><span class="arrow">&gt;</span> node ready — accepting requests</div>
                </div>
            </div>

            <div>
                <div class="stats">
                    <div class="stat-card" style="--accent: var(--blue);">
                        <div class="label">SERVER TIME (UTC)</div>
                        <div class="value" id="server-time">{{ current_time }}</div>
                    </div>
                    <div class="stat-card" style="--accent: var(--green);">
                        <div class="label">ENVIRONMENT HEALTH</div>
                        <div class="value" style="color: var(--green);">Nominal</div>
                    </div>
                    <div class="stat-card" style="--accent: var(--orange);">
                        <div class="label">ENVIRONMENT NAME</div>
                        <div class="value">{{ env_name }}</div>
                    </div>
                    <div class="stat-card" style="--accent: var(--magenta);">
                        <div class="label">SERVICE ID</div>
                        <div class="value">slt-mobitel-cloud-01</div>
                    </div>
                </div>

                <div class="actions">
                    <a href="/health" class="btn btn-primary">Run health check</a>
                    <a href="{{ github_url }}" target="_blank" class="btn btn-outline">
                        <svg height="16" width="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path></svg>
                        View source on GitHub
                    </a>
                </div>
            </div>

        </div>
    </main>

    <footer>SLT MOBITEL CLOUD &nbsp;·&nbsp; AWS Elastic Beanstalk &nbsp;·&nbsp; Flask {{ flask_note }}</footer>

</body>
</html>
"""


@application.route('/')
def home():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    env_name = os.environ.get('AWS_EB_ENVIRONMENT_NAME', 'LOCAL_DEBUG')
    aws_region = os.environ.get('AWS_REGION', 'ap-south-1')

    return render_template_string(
        HTML_TEMPLATE,
        current_time=now,
        github_url=GITHUB_REPO_URL,
        env_name=env_name,
        aws_region=aws_region,
        flask_note='v3.x'
    )


@application.route('/health')
def health_check():
    return jsonify({
        "status": "nominal",
        "service_id": "slt-mobitel-cloud-01",
        "timestamp_utc": datetime.utcnow().isoformat()
    }), 200


if __name__ == '__main__':
    # Local development server execution
    application.run(host='0.0.0.0', port=5000)
