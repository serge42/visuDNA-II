package geneStruct;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * @author Maria Sisto
 * 
 * Uses parser to add interactions in the interactome.
 */
class InteractionsFiller {

	public InteractionsFiller(InteractionsParser parsei, Interactome interactome) {
		Map<Integer, Gene> genes = new HashMap<Integer, Gene>();
		Set<Interaction> interactions = new HashSet<Interaction>();
		
		Interaction interaction;
		while((interaction = parsei.next()) != null) {
			interactions.add(interaction);
			genes.put(interaction.getG1().getID(), interaction.getG1());
			genes.put(interaction.getG2().getID(), interaction.getG2());
		}
		interactome.setInteractions(interactions);
	}
}