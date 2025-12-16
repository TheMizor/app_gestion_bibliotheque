const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Dans Docker, utiliser le nom du service backend
  // En développement local sans Docker, utiliser localhost
  const backendUrl = 'http://backend:5000';
  
  console.log(`Setting up proxy to backend at: ${backendUrl}`);
  
  // Proxy pour les requêtes API vers le backend
  // WS à false pour éviter d'intercepter le hot-reload de React
  app.use(
    '/api',
    createProxyMiddleware({
      target: backendUrl,
      changeOrigin: true,
      secure: false,
      ws: false, 
      logLevel: 'debug',
      timeout: 30000, // Timeout de 30 secondes
      proxyTimeout: 30000,
      onProxyReq: (proxyReq, req, res) => {
        console.log(`[PROXY] ${req.method} ${req.url} -> ${backendUrl}${req.url}`);
      },
      onProxyRes: (proxyRes, req, res) => {
        console.log(`[PROXY] Response ${proxyRes.statusCode} for ${req.url}`);
      },
      onError: (err, req, res) => {
        console.error('[PROXY ERROR]', err.message);
        console.error('[PROXY ERROR] Details:', err);
        if (!res.headersSent) {
          res.status(503).json({ 
            error: 'Service unavailable', 
            message: 'Cannot connect to backend server',
            details: err.message 
          });
        }
      }
    })
  );
};

