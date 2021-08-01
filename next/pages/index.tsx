import Head from 'next/head'
import styles from '../styles/Home.module.css'
import { GetStaticProps } from 'next'
import Link from 'next/link'
import React, { FC } from 'react'
import path from 'path';
import glob from 'glob'

type ListProps = { fileNames: string[] }

const List: FC<ListProps> = ({ fileNames }) => {
  return <>{fileNames && fileNames.map((fileName) => <Link href={`music/${fileName.split('.')[0]}`} key={fileName}><a>{fileName}</a></Link>)}</>
}

export const getStaticProps: GetStaticProps = async () => {
  const fileNames = glob.sync(path.join(process.cwd(), './public/sunvox', '**/*.sunvox')).map((path) => (path.split('/sunvox/')[1]))
  const props: ListProps = { fileNames }
  return { props }
}

const Home = ({ fileNames }) => {
  return (
    <div className={styles.container}>
      <Head>
        <title>Sunvox Models</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Sunvox Music
        </h1>
        <List {...{ fileNames }} />
      </main>

      <footer className={styles.footer}>
        <a
          href="https://www.cactice.com"
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

export default Home
