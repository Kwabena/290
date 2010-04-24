#!/usr/bin/ruby

#these procedures are painfully slow because of how wget works
#it will take about 30 seconds to create a graph with
#20 nodes (vertices) on a Zoo machine whose specs I'm yet to figure out

def max(num1, num2)
  num1 > num2 ? num1 : num2
end

def follow(f)
  #follow a Youtube video and return an array of all the related 
  #videos (usually 20) each video has a unique eleven character 
  #id so return it in the format
  #http://www.youtube.com/watch?v=elevenchrid (which is also the format of f)
  %x{rm -rf www.youtube.com}
  %x{wget -r -l 1 #{f} 2> /dev/null}  #redirect ouput (to stderr) to dummy file
  res = []
  if Dir.entries(".").index("www.youtube.com")
    res = Dir.entries("www.youtube.com")
  end
  res = res.select {|x|  x =~ /(watch\?v=.{11})&feature=related/}
  root = "http://www.youtube.com/"
  res.map! {|x|  (x =~ /(watch\?v=.{11})/) && (root + $&)}
end

#for f in ARGV
#  for file in follow(f)
#    puts file
#  end
#end

#start from video v and generate a graph with a little > N edges
def generateGraph(v, n)
  g = []
  nodes = [v]
  hash = {}
  hash[v] = nodes.index(v)
  for node in nodes
    if g.size < n
      curr_node_id = nodes.index(node)
      next_gen = follow(node)
      
      for vertex in next_gen
        num = hash[vertex]
        if num
          #g << [curr_node_id, num]
        else
          nodes << vertex
          num = nodes.index(vertex)
          hash[vertex] = num
        end
         g << [curr_node_id, num]
         puts "#{curr_node_id} #{num}"
      end
    else
      return g
    end
  end
end


#start from a video and generate a graph with about N nodes
def generateGraph2(v, n, file)
  f = File.open(file, 'w')
  g = []
  nodes = [v]
  hash = {}
  hash[v] = nodes.index(v)
  max_node_id = 0
  for node in nodes
    curr_node_id = nodes.index(node)
    if max_node_id < n
      next_gen = follow(node)
      
      for vertex in next_gen
        num = hash[vertex]
        if num
          #g << [curr_node_id, num]
        else
          nodes << vertex
          num = nodes.index(vertex)
          hash[vertex] = num
        end
          #g << [curr_node_id, num]
          f.puts "#{curr_node_id} #{num}"
          puts "#{curr_node_id} #{num}"
          max_node_id = max(max_node_id, num)
      end
    else
      #return g
    end
  end
end

#generateGraph2("http://www.youtube.com/watch?v=rNxX0-FVW1M", 100)

generateGraph2(ARGV[0], ARGV[1].to_i, ARGV[2])
