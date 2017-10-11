package geneStruct;

import java.io.FileNotFoundException;
import java.io.IOException;

class Main {
	public static void main(String[] args) {

		String pathI = "sources/interactome.tsv";
		String pathG = "sources/annotations.tsv";

		try {
			Interactome interactome = new Interactome(new InteractionParserTSV(pathI)); // Creates the interactome
			
			new AnnotationsFiller(new AnnotationsParserTSV(pathG), interactome); // Adds annotations on interactome
			
			new GMLWriter(interactome).write("sources/test.gml", "Test graph"); // Writes interactome into file
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
}