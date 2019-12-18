package edu.gatech.cse6242;

import java.io.IOException;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1 {
	public static class TokenizerMapper
    extends Mapper<Object, Text, Text, Text>{

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

            String[] line = value.toString().split("\t");
            if(line.length ==3) {
                String source = line[0];
                String target = line[1];
				String weight = line[2];

                context.write(new Text(source),new Text(target+","+weight));
            }
        }
    }

    public static class TextSumReducer
    extends Reducer<Text,Text,Text,Text> {
        
        public void reduce(Text key, Iterable<Text> values,
                           Context context
                           ) throws IOException, InterruptedException {
            int sofar = 0;
            int target = 0;
            for (Text value : values) {
                String[] tokens = value.toString().split(",");
                
                if(Integer.parseInt(tokens[1])>sofar) {
                    sofar = Integer.parseInt(tokens[1]);
                    target=Integer.parseInt(tokens[0]);}

                else if(Integer.parseInt(tokens[1])==sofar) {
                    if (Integer.parseInt(tokens[0])<target){
                        target=Integer.parseInt(tokens[0]);}
                }
            }
                context.write(key, new Text(Integer.toString(target)+","+Integer.toString(sofar)));
            
        }
    }


  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1");

    /* TODO: Needs to be implemented */
    	job.setJarByClass(Q1.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(TextSumReducer.class);
        job.setReducerClass(TextSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
