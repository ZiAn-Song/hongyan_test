export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const backendUrl = env.BACKEND_URL || 'http://localhost:8000';
  const targetUrl = backendUrl + '/api' + url.pathname.replace(/^\/api/, '') + url.search;

  const headers = new Headers(request.headers);
  headers.set('Host', new URL(backendUrl).host);

  const fetchOptions = {
    method: request.method,
    headers: headers,
  };

  if (request.method !== 'GET' && request.method !== 'HEAD') {
    fetchOptions.body = await request.arrayBuffer();
  }

  const response = await fetch(targetUrl, fetchOptions);

  const responseHeaders = new Headers(response.headers);
  responseHeaders.set('Access-Control-Allow-Origin', '*');
  responseHeaders.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  responseHeaders.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: responseHeaders });
  }

  return new Response(response.body, {
    status: response.status,
    headers: responseHeaders,
  });
}
