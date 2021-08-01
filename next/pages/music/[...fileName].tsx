import glob from 'glob';
import { GetStaticProps } from "next";
import { useRouter } from 'next/router';
import path from 'path';
import { basePath } from '~/constants';

const ModelPage = () => {
  const router = useRouter()
  const { fileName } = router.query

  const singleFileName =
    typeof fileName === 'string' ?
      fileName
      : fileName.join('/')

  return (<>
    <p style={{ textAlign: 'center' }}>{singleFileName}</p>
    <iframe src={`${basePath}/sunvox_frame.html?file=sunvox/${singleFileName}.sunvox`} style={{
      display: 'block',
      border: 'none',
      height: '100vh',
      width: '100vw'
    }} />
  </>
  )
}

export const getStaticPaths = async () => {
  const paths = glob.sync(
    path.join(process.cwd(), './public/sunvox', '**/*.sunvox')
  ).map((path) => (
    {
      params: { fileName: path.split('/sunvox/')[1].split('.')[0].split('/') }
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
