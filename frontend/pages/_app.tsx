import type { AppProps } from 'next/app';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import Cookies from 'js-cookie';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter();

  useEffect(() => {
    const token = Cookies.get('token');
    const publicPages = ['/login', '/register'];
    
    if (!token && !publicPages.includes(router.pathname)) {
      router.push('/login');
    } else if (token && publicPages.includes(router.pathname)) {
      router.push('/dashboard');
    }
  }, [router.pathname]);

  return <Component {...pageProps} />;
}