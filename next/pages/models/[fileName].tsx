import * as fs from "fs";
import path from 'path';

export async function getStaticPaths() {
  const pagesDirectory = path.resolve(process.cwd(), 'pages');
  const fileNames = fs.readdirSync(path.join(pagesDirectory, '../public/glb'))
  const paths= fileNames.map((fileName)=>({params:{fileName}))
  return {
    paths ,
    fallback: false
  };
}
