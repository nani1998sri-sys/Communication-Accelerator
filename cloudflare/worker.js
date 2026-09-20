export default {
  async scheduled(event, env, ctx) { ctx.waitUntil(triggerGitHubWorkflow(env)); },
  async fetch(request, env) {
    if (request.method !== "POST" || request.headers.get("X-Cron-Secret") !== env.CRON_SHARED_SECRET) return new Response("Not found", {status: 404});
    await triggerGitHubWorkflow(env); return new Response("Workflow triggered", {status: 202});
  }
};
async function triggerGitHubWorkflow(env) {
  const url = `https://api.github.com/repos/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/actions/workflows/${env.GITHUB_WORKFLOW_ID}/dispatches`;
  const response = await fetch(url, {method: "POST", headers: {"Authorization": `Bearer ${env.GITHUB_TOKEN}`, "Accept": "application/vnd.github+json", "Content-Type": "application/json", "User-Agent": "communication-coach-backup"}, body: JSON.stringify({ref: env.GITHUB_REF || "main"})});
  if (!response.ok) throw new Error(`GitHub dispatch failed: ${response.status}`);
}
