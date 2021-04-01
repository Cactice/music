import { GetStaticProps } from 'next'
import { FC } from 'react'
import * as fs from "fs";
import path from 'path';

type ListProps = { fileNames: string[] }

export const List: FC<ListProps> = ({ fileNames }) => {
  return <>{fileNames && fileNames.map((fileName) => <a href={`models/${fileName}`}>Post: {fileName}</a>)}</>
}

export const getStaticProps: GetStaticProps = async () => {
  const pagesDirectory = path.resolve(process.cwd(), 'pages');
  const fileNames = fs.readdirSync(path.join(pagesDirectory, '../public/glb'))
  const props: ListProps = { fileNames }
  return { props }
}

export default List
