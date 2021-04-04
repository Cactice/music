import * as fs from "fs";
import { GetStaticProps } from "next";
import dynamic from "next/dynamic";
import { useRouter } from 'next/router';
import path from 'path';
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
  const fileNames = fs.readdirSync(path.join(process.cwd(), './public/glb'))
  const paths = fileNames.filter(
    (fileName) => fileName.endsWith('.glb')
  ).map((fileName) => ({
    params: { fileName: fileName.split('.')[0] }
  }))
  return {
    paths,
    fallback: false
  };
}
export const getStaticProps: GetStaticProps = async () => {
  return { props: {} }
}

export default ModelPage
