package geneStruct;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * @author Maria Sisto
 *
 * Represents an interactome, including collection of interactions and annotations.
 */
class Interactome {
	private Set<Interaction> interactions = new HashSet<Interaction>();
	private Map<Integer, Gene> genes = new HashMap<Integer, Gene>();

	/**
	 * Constructor. Fills the interactions Set.
	 * @param interactP
	 * @throws FileNotFoundException
	 * @throws IOException
	 * @throws Exception
	 */
	public Interactome(InteractionsParser interactP) throws FileNotFoundException, IOException, Exception {
		new InteractionsFiller(interactP, this);
	}

	public Map<Integer, Gene> getGenes() {
		return genes;
	}

	public Set<Interaction> getInteractions() {
		return interactions;
	}

	public void setGenes(Map<Integer, Gene> genes) {
		this.genes = genes;
	}

	public void setInteractions(Set<Interaction>interactions) {
		this.interactions = interactions;
	}
}