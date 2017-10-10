package geneStruct;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.StringTokenizer;

/**
 * @author Maria Sisto
 * 
 * Specific interaction parser.
 */
class InteractionParserTSV  implements InteractionsParser {
	private String separator = "\t";
	private int fromLine = 2;
	private BufferedReader file;
	private int gIDPos1 = 1;
	private int gNamePos1 = 2;
	private int gIDPos2 = 3;
	private int gNamePos2 = 4;

	private boolean print = true;
	
	public InteractionParserTSV(String path) throws FileNotFoundException, IOException {
		file = new BufferedReader(new FileReader(path));
		for (int i = 1; i < fromLine; i++) { // Skip first lines
			file.readLine();
		}
	}
	
	/* Returns next gene in file */
	public Interaction next() {
		String line;
		try {
			line = file.readLine();
			if (line != null){
				StringTokenizer st = new StringTokenizer(line, separator);
				int i = 1;
				int geneID1 = 0;
				String geneName1 = "";
				int geneID2 = 0;
				String geneName2 = "";
				
				while (st.hasMoreTokens()) {
					String token = st.nextToken();
					if (i == gIDPos1 ) {
						geneID1 = Integer.parseInt(token);
						if (print) System.out.print(token + " ");
					} else if (i == gNamePos1 ) {
						geneName1 = token;
						if (print) System.out.print(token + " ");
					} if (i == gIDPos2 ) {
						geneID2 = Integer.parseInt(token);
						if (print) System.out.print(token + " ");
					} else if (i == gNamePos2 ) {
						geneName2 = token;
						if (print) System.out.print(token + " ");
					}
					
					i++;
				}
				if (print) System.out.println();
				 return new Interaction(new Gene(geneID1, geneName1), new Gene(geneID2, geneName2));
				 
			} else {
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