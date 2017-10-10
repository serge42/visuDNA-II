package geneStruct;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.Map;
import java.util.Set;

/**
 * @author Maria Sisto
 *
 * Writes the interactome in gml format.
 */
class GMLWriter implements GraphWriter{
	private Interactome interactome;

	public GMLWriter(Interactome interactome) throws FileNotFoundException, UnsupportedEncodingException {
		this.interactome = interactome;
	}

	public void write (String outputPath, String label) throws FileNotFoundException, UnsupportedEncodingException {
		PrintWriter writer = new PrintWriter(outputPath, "UTF-8");
		
		Set<Interaction> interactions = interactome.getInteractions();
		Map<Integer, Gene> genes = interactome.getGenes();
		writer.println("graph [");
		writer.println("comment \" " + label + " \"");
		writer.println("directed 1");
		writer.println("label \" " + label + " \"");
		
		// Writes the genes
		for (Gene g : genes.values()) {
			writer.println("node [");
			writer.println("id " + g.getID());
			writer.println("ID " + g.getID());
			writer.println("label \"" + g.getName() + "\"");
			int i = 0;
			for (String s : g.getPhenotype()) {
				writer.println("phyenotype" + (i++) + " \"" + s + "\"");
			}
			writer.println("]");
		}
		
		// Writes the interactions
		for (Interaction intr : interactions) {
			writer.println("edge [");
			writer.println("source " + intr.getG1().getID());
			writer.println("target " + intr.getG2().getID());
			writer.println("]");
		}
		writer.println("]");
		writer.close();
	}
}