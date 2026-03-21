import { useState, useEffect, useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  MarkerType,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

function FlowNode({ data }) {
  const { label, nodeType, isActive, isPast, isDark } = data;

  const colors = {
    start: '#22c55e', end: '#ef4444', process: '#6366f1',
    loop: '#f59e0b', condition: '#3b82f6', output: '#14b8a6',
  };
  const color = colors[nodeType] || colors.process;
  const radius = nodeType === 'start' || nodeType === 'end' ? '50%' : nodeType === 'condition' ? '10px' : '8px';

  const inactiveText = isDark ? '#64748b' : '#94a3b8';
  const pastText = isDark ? '#cbd5e1' : '#475569';

  return (
    <div style={{
      background: isActive ? color : isPast ? `${color}22` : `${color}11`,
      border: `2px solid ${isActive ? color : isPast ? `${color}55` : `${color}30`}`,
      borderRadius: radius,
      padding: '8px 16px',
      color: isActive ? '#fff' : isPast ? pastText : inactiveText,
      fontSize: '0.72rem',
      fontFamily: "'JetBrains Mono', monospace",
      fontWeight: isActive ? 700 : 400,
      textAlign: 'center',
      transition: 'all 0.25s ease',
      boxShadow: isActive ? `0 0 16px ${color}50` : 'none',
      transform: isActive ? 'scale(1.1)' : 'scale(1)',
      minWidth: 70,
    }}>
      {label}
    </div>
  );
}

const nodeTypes = { flowNode: FlowNode };

function buildFlowGraph(code) {
  const lines = code.split('\n');
  const nodes = [];
  const edges = [];
  let id = 0;
  const makeId = () => `n${id++}`;

  const startId = makeId();
  nodes.push({ id: startId, type: 'start', label: 'Start', line: 0 });
  let prevId = startId;

  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const lineNum = i + 1;
    let nodeType = 'process';
    let label = trimmed;
    if (trimmed.startsWith('for ') || trimmed.startsWith('while ')) { nodeType = 'loop'; label = trimmed.replace(':', ''); }
    else if (trimmed.startsWith('if ') || trimmed.startsWith('elif ')) { nodeType = 'condition'; label = trimmed.replace(':', ''); }
    else if (trimmed.startsWith('else:')) { nodeType = 'condition'; label = 'else'; }
    else if (trimmed.startsWith('print(')) { nodeType = 'output'; }
    if (label.length > 28) label = label.slice(0, 26) + '…';
    const nid = makeId();
    nodes.push({ id: nid, type: nodeType, label, line: lineNum });
    edges.push({ from: prevId, to: nid });
    prevId = nid;
  }

  const endId = makeId();
  nodes.push({ id: endId, type: 'end', label: 'End', line: 9999 });
  edges.push({ from: prevId, to: endId });
  return { nodes, edges };
}

export default function FlowDiagram({ code, currentLine, steps, currentStep, isDark }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const graph = useMemo(() => buildFlowGraph(code), [code]);

  const visitedLines = useMemo(() => {
    const s = new Set();
    if (steps && currentStep >= 0) {
      for (let i = 0; i <= currentStep; i++) s.add(steps[i].line);
    }
    return s;
  }, [steps, currentStep]);

  useEffect(() => {
    const edgeColor = isDark ? '#334155' : '#cbd5e1';

    const rfNodes = graph.nodes.map((n, i) => ({
      id: n.id,
      type: 'flowNode',
      position: { x: 60, y: i * 72 },
      data: {
        label: n.label, nodeType: n.type, line: n.line, isDark,
        isActive: n.line === currentLine,
        isPast: visitedLines.has(n.line),
      },
    }));

    const rfEdges = graph.edges.map((e, i) => {
      const src = graph.nodes.find(n => n.id === e.from);
      const tgt = graph.nodes.find(n => n.id === e.to);
      const isActive = src?.line === currentLine || tgt?.line === currentLine;
      const isPast = visitedLines.has(src?.line) && visitedLines.has(tgt?.line);
      return {
        id: `e${i}`, source: e.from, target: e.to, type: 'smoothstep',
        animated: isActive,
        style: { stroke: isActive ? '#6366f1' : isPast ? '#6366f155' : edgeColor, strokeWidth: isActive ? 2.5 : 1.5 },
        markerEnd: { type: MarkerType.ArrowClosed, color: isActive ? '#6366f1' : edgeColor, width: 12, height: 12 },
      };
    });

    setNodes(rfNodes);
    setEdges(rfEdges);
  }, [graph, currentLine, visitedLines, isDark, setNodes, setEdges]);

  if (nodes.length === 0) return <div className="flex items-center justify-center h-full text-text3 text-xs">Write code to see flow</div>;

  return (
    <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}
      nodeTypes={nodeTypes} fitView fitViewOptions={{ padding: 0.2 }}
      proOptions={{ hideAttribution: true }} minZoom={0.3} maxZoom={1.5}
      style={{ background: 'transparent' }}>
      <Background color={isDark ? '#1e293b' : '#e2e8f0'} gap={20} size={1} />
      <Controls showInteractive={false} style={{ background: isDark ? '#1e293b' : '#f1f5f9', borderColor: isDark ? '#334155' : '#e2e8f0', borderRadius: 6 }} />
    </ReactFlow>
  );
}
