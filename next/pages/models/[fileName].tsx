import * as fs from "fs";
import path from 'path';
import { useRouter } from 'next/router'
import { GetStaticProps } from "next";
type ListProps = { fileNames: string[] }

const ModelPage = () => {
  const router = useRouter()
  const { fileName } = router.query

  return <p>Post: {fileName}</p>

}

export const getStaticPaths = async () => {
  const pagesDirectory = path.resolve(process.cwd(), 'pages');
  const fileNames = fs.readdirSync(path.join(pagesDirectory, '../public/glb'))
  const paths = fileNames.map((fileName) => ({ params: { fileName } }))
  return {
    paths,
    fallback: false
  };
}
export const getStaticProps: GetStaticProps = async () => {
  const pagesDirectory = path.resolve(process.cwd(), 'pages');
  const fileNames = fs.readdirSync(path.join(pagesDirectory, '../public/glb'))
  const props: ListProps = { fileNames }
  return { props }
}

export default ModelPage
