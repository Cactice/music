import * as fs from "fs";
import { GetStaticProps } from "next";
import dynamic from "next/dynamic";
import { useRouter } from 'next/router';
import path from 'path';
import glob from 'glob'
import { basePath } from '~/constants'
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
      : fileName.join('/')

  return (<>
    <p>{singleFileName}</p>
    <Model fileName={`${basePath}/glb/${singleFileName}.glb`} />
  </>
  )
}

export const getStaticPaths = async () => {
  const paths = glob.sync(
    path.join(process.cwd(), './public/glb', '**/*.glb')
  ).map((path) => (
    {
      params: { fileName: path.split('/glb/')[1].split('.')[0].split('/') }
    }
  ))
  return {
    paths,
    fallback: false
  };
}

export const getStaticProps: GetStaticProps = async () => {
  return { props: {} }
}

export default ModelPage
