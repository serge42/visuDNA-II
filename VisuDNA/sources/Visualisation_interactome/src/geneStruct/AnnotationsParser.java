package geneStruct;

/**
 * @author Maria Sisto
 * 
 * Interface for parsers parsing files containing genes and their annotations.
 */
interface AnnotationsParser {

	/**
	 * @return Next Gene in file
	 */
	public Gene next();
}