const backendUrl = process.env.FLASK_API_URL || "http://127.0.0.1:5200";

const nextConfig = {
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${backendUrl}/api/:path*` }];
  },
};

export default nextConfig;
