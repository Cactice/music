import * as fs from "fs";
import path from 'path';
import { useRouter } from 'next/router'
import { GetStaticProps } from "next";
type ListProps = { fileNames: string[] }
import { NoSsr } from '~/components/nossr'
import dynamic from "next/dynamic";
const Model = dynamic(
  () => import('~/components/model'),
  { ssr: false }
)
const ModelPage = () => {
  const router = useRouter()
  const { fileName } = router.query

  const singleFileName =
    typeof fileName === 'string' ?
      fileName
      : fileName[0]

  return (<>
    <p>{singleFileName}</p>
    <Model fileName={`/glb/${singleFileName}.glb`} />
  </>
  )
}

export const getStaticPaths = async () => {
  const pagesDirectory = path.resolve(process.cwd(), 'pages');
  const fileNames = fs.readdirSync(path.join(pagesDirectory, '../public/glb'))
  const paths = fileNames.map((fileName) => ({ params: { fileName: fileName.split('.')[0] } }))
  return {
    paths,
    fallback: false
  };
}
export const getStaticProps: GetStaticProps = async () => {
  return { props: {} }
}

export default ModelPage
