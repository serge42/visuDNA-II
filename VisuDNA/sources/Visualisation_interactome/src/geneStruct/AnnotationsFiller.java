package geneStruct;

import java.util.Map;

/**
 * @author Maria Sisto
 * 
 * Uses parser to add annotations about the genes in the interactome.
 */
class AnnotationsFiller {
	public AnnotationsFiller(AnnotationsParser parseg, Interactome interactome) {
		Map<Integer, Gene> genes = interactome.getGenes(); // Retrieves genes in the interactome.

		Gene gene;
		while ((gene = parseg.next()) != null) {
			if (genes.containsKey(gene.getID())) { // If the genes is in interactome, add the new phenotype to the gene in the final gene list
				genes.get(gene.getID()).addPhenotype(gene.getPhenotype());
			} else {
				System.err.println("Warning:  gene " + gene.getID() + " not present in interactom.");
			}
		}
	}
}