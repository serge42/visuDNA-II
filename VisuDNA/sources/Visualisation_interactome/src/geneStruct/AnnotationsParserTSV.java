package geneStruct;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.StringTokenizer;

/**
 * @author Maria Sisto
 *
 * Specific annotation parser.
 */
class AnnotationsParserTSV  implements AnnotationsParser {
	private String separator = "\t";
	private int fromLine = 2;
	private BufferedReader file;
	private int gIDPos = 3;
	private int gNamePos = 4;
	private int gPhenoPos = 2;

	private boolean print = true;
	
	public AnnotationsParserTSV(String path) throws FileNotFoundException, IOException {
		file = new BufferedReader(new FileReader(path));
		for (int i = 1; i < fromLine; i++) { // Skip first lines
			file.readLine();
		}
	}
	
	public Gene next() {
		String line;
		try {
			line = file.readLine();
			if (line != null){
				StringTokenizer st = new StringTokenizer(line, separator);
				int i = 1;
				int geneID = 0;
				String geneName = "";
				String genePhenotype = "";
				
				while (st.hasMoreTokens()) {
					String token = st.nextToken();
					if (i == gIDPos ) {
						geneID = Integer.parseInt(token);
						if (print) System.out.print(token + " ");
					} else if (i == gNamePos ) {
						geneName = token;
						if (print) System.out.print(token + " ");
					} else if (i == gPhenoPos ) {
						genePhenotype = token;
						if (print) System.out.print(token + " ");
					}
					
					i++;
				}
				if (print) System.out.println();
				ArrayList<String> p = new ArrayList<String>();
				p.add(genePhenotype);
				return new Gene(geneID, geneName, p);
			} else { // If we reach the end of the file, the file is closed
				file.close();
				return null;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		};
		return null;
	}
}