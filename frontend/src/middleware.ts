import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const url = request.nextUrl.clone();

  // check for token
  const token = request.cookies.get("auth_token");

  if (!token) {
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }

  // progress if authenticated
  return NextResponse.next();
}

export const config = { matcher: ["/:path*"] };
