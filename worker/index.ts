interface Env {
  ASSETS: {
    fetch(request: Request): Promise<Response>;
  };
}

const worker = {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/index.html") {
      url.pathname = "/";
      return Response.redirect(url, 308);
    }

    if (url.pathname === "/epk") {
      url.pathname = "/epk/";
      return Response.redirect(url, 308);
    }

    const publicPath =
      url.pathname === "/"
        ? "/site/index.html"
        : url.pathname === "/epk/"
          ? "/site/epk/index.html"
          : `/site${url.pathname}`;

    return env.ASSETS.fetch(new Request(new URL(publicPath, request.url), request));
  },
};

export default worker;
