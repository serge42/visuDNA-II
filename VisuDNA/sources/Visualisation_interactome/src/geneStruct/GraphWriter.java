package geneStruct;

import java.io.FileNotFoundException;
import java.io.UnsupportedEncodingException;

/**
 * @author Maria Sisto
 *
 * Interface for writing an interactome into a graph.
 */
interface GraphWriter {
	public void write (String outputPath, String label) throws FileNotFoundException, UnsupportedEncodingException;
}