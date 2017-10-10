package geneStruct;

/**
 * @author Maria Sisto
 *
 * Interface for parsers parsing files containing interactions between genes.
 */
interface InteractionsParser {
	public Interaction next();
}