import Head from 'next/head'
import styles from '../styles/Home.module.css'
import { GetStaticProps } from 'next'
import Link from 'next/link'
import React, { FC } from 'react'
import path from 'path';
import glob from 'glob'
type ListProps = { fileNames: string[] }

const List: FC<ListProps> = ({ fileNames }) => {
  return <>{fileNames && fileNames.map((fileName) => <Link href={`models/${fileName.split('.')[0]}`} key={fileName}><a>{fileName}</a></Link>)}</>
}

export const getStaticProps: GetStaticProps = async () => {
  const fileNames = glob.sync(path.join(process.cwd(), './public/glb', '**/*.glb')).map((path) => (path.split('/glb/')[1]))
  const props: ListProps = { fileNames }
  return { props }
}

export default function Home({ fileNames }) {
  return (
    <div className={styles.container}>
      <Head>
        <title>Create Next App</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="https://nextjs.org">Next.js!</a>
        </h1>
        <List {...{ fileNames }} />
      </main>

      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          Cactice
        </a>
      </footer>
    </div>
  )
}
