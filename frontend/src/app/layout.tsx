import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Data Analyst",
  description: "AI-powered data analysis platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
