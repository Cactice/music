import * as fs from "fs";
import path from 'path';

export const ModelPage = () => {
  const router = useRouter()
  const { fileName } = router.query

  return <p>Post: {fileName}</p>

}

export const getStaticPaths = async () => {
  const pagesDirectory = path.resolve(process.cwd(), 'pages');
  const fileNames = fs.readdirSync(path.join(pagesDirectory, '../public/glb'))
  const paths = fileNames.map((fileName) => ({ params: { fileName }))
  return {
    paths,
    fallback: false
  };
}
function useRouter() {
  throw new Error("Function not implemented.");
}
