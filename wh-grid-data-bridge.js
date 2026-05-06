/**
 * wh-grid-data-bridge.js
 * ──────────────────────
 * Shared data ingestion module for the WH-Grid instrument family.
 * Fetches worldtext-program-theory.json and github-ripple-index.json,
 * then maps them into the archiveTiers / archiveClusters / archiveBlocks /
 * leafTemplates shape that all wh-grid render engines expect.
 *
 * Usage:
 *   <script src="wh-grid-data-bridge.js"></script>
 *   <script>
 *     whBridge.boot(function(data) {
 *       // data.archiveTiers, data.archiveClusters, data.archiveBlocks,
 *       // data.leafTemplates, data.repos, data.domains, data.clusters,
 *       // data.works
 *     });
 *   </script>
 */
(function (root) {
  'use strict';

  var PT_URL  = 'worldtext-program-theory.json';
  var REPO_URL = 'github-ripple-index.json';

  function fetchJSON(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error(url + ' → ' + r.status);
      return r.json();
    });
  }

  /**
   * Map the theory JSON (9 tiers, 35 nodes) into the 3-domain / 9-cluster /
   * 18-block / 36-leaf structure the canonical wh-grid files expect.
   */
  function mapTheoryToCanonical(pt) {
    var tiers   = pt.archive_tiers || [];
    var domains = [];
    var clusterArr = [];
    var blockArr   = [];
    var leafArr    = [];

    // ── GROUP tiers into 3 domains (Research / Instruments / Public Work) ──
    var domainMap = [
      { name: 'Research',     color: '#ff6b35', tierIds: [] },
      { name: 'Instruments',  color: '#e76f51', tierIds: [] },
      { name: 'Public Work',  color: '#457b9d', tierIds: [] }
    ];

    tiers.forEach(function (t, i) {
      var bucket = i < 3 ? 0 : i < 6 ? 1 : 2;
      domainMap[bucket].tierIds.push(i);
    });

    var dIdx = 0, cIdx = 0, bIdx = 0, lIdx = 0;

    domainMap.forEach(function (dm) {
      dIdx++;
      var dId = 'D' + dIdx;
      var cIds = [];

      dm.tierIds.forEach(function (ti) {
        var tier = tiers[ti];
        if (!tier) return;
        cIdx++;
        var cId = 'C' + cIdx;
        cIds.push(cId);
        var bIds = [];
        var nodes = tier.nodes || [];

        // Two blocks per cluster (or 1 if only 1 node)
        var half = Math.ceil(nodes.length / 2);
        for (var g = 0; g < 2; g++) {
          var slice = g === 0 ? nodes.slice(0, half) : nodes.slice(half);
          if (slice.length === 0) continue;
          bIdx++;
          var bId = 'B' + bIdx;
          bIds.push(bId);
          var leafIds = [];

          slice.forEach(function (node) {
            lIdx++;
            var lId = String(lIdx).padStart(2, '0');
            leafIds.push(lId);
            leafArr.push([
              node.kicker || node.role || 'Node',
              node.thesis || node.title || 'Worldtext node.'
            ]);
          });

          blockArr.push({
            id: bId,
            cluster: cId,
            name: slice[0].kicker || tier.tier_name,
            title: slice.map(function (n) { return n.title; }).join(' / '),
            url: slice[0].url || '#',
            leaves: leafIds,
            _nodes: slice  // preserve raw nodes for extended access
          });
        }

        clusterArr.push({
          id: cId,
          domain: dId,
          name: tier.tier_name.replace(/^(Current |Operative |Legacy |Cultural |Synthetic )/, ''),
          blocks: bIds,
          _tier: tier
        });
      });

      domains.push({
        id: dId,
        name: dm.name,
        clusters: cIds,
        desc: dm.name + ' — ' + cIds.length + ' clusters, mapped from ' + dm.tierIds.length + ' tiers.'
      });
    });

    return {
      archiveTiers:    domains,
      archiveClusters: clusterArr,
      archiveBlocks:   blockArr,
      leafTemplates:   leafArr,
      _rawPT: pt
    };
  }

  /**
   * Map the repo JSON (311 repos) into the flat repos[] array
   * that wh-grid-05.html and wh-grid-pipe.html expect.
   */
  function mapReposToFlat(repoData, canonical) {
    var allRepos = repoData.all_repos || [];
    var domainNames  = canonical.archiveTiers.map(function (d) { return d.name; });
    var clusterNames = canonical.archiveClusters.map(function (c) { return c.name; });
    var workNames    = canonical.archiveBlocks.map(function (b) { return b.name; });

    var colors = ['#f46034','#ef8b16','#efc400','#8bc52a','#58b987','#3ca7d8','#db3d37'];

    return allRepos.map(function (r, i) {
      // Assign domain/cluster/work by ring-bucketing
      var dI = i % domainNames.length;
      var cI = i % clusterNames.length;
      var wI = i % workNames.length;
      return {
        id:      i + 1,
        slug:    r.name,
        title:   r.name.replace(/-/g, ' '),
        domain:  domainNames[dI],
        cluster: clusterNames[cI],
        work:    workNames[wI],
        color:   colors[i % colors.length],
        lang:    r.language || 'txt',
        date:    (r.updated_at || r.created_at || '2026-01-01').split('T')[0],
        claim:   r.description || (r.name + ' is an addressable payload inside the worldtext practice archive.'),
        url:     r.homepage || r.html_url || '#',
        stars:   r.stars || 0,
        forks:   r.forks || 0,
        html_url: r.html_url || '#'
      };
    });
  }

  /**
   * Boot: fetch data → map → call back.
   */
  function boot(callback) {
    var ptSource   = root.__PT_DATA  ? Promise.resolve(root.__PT_DATA)  : fetchJSON(PT_URL);
    var repoSource = root.__REPO_DATA ? Promise.resolve(root.__REPO_DATA) : fetchJSON(REPO_URL);

    Promise.all([ptSource, repoSource]).then(function (results) {
      var pt   = results[0];
      var repo = results[1];

      root.__PT_DATA   = pt;
      root.__REPO_DATA = repo;

      var canonical = mapTheoryToCanonical(pt);
      var repos     = mapReposToFlat(repo, canonical);

      // Build derived arrays for wh-grid-05 / ant-01 style files
      var domainNames  = canonical.archiveTiers.map(function (d) { return d.name; });
      var clusterNames = canonical.archiveClusters.map(function (c) { return c.name; });
      var workNames    = canonical.archiveBlocks.map(function (b) { return b.name; });

      var out = {
        archiveTiers:    canonical.archiveTiers,
        archiveClusters: canonical.archiveClusters,
        archiveBlocks:   canonical.archiveBlocks,
        leafTemplates:   canonical.leafTemplates,
        repos:           repos,
        domains:         domainNames,
        clusters:        clusterNames,
        works:           workNames,
        _rawPT:          pt,
        _rawRepo:        repo
      };

      if (typeof callback === 'function') callback(out);
    }).catch(function (err) {
      console.error('[wh-grid-data-bridge] Boot failed:', err);
    });
  }

  root.whBridge = { boot: boot };

})(window);
