<template>
  <div class="page">
    <AppHeader />

    <section class="page-header">
      <div class="container">
        <h1>
          <i class="fas fa-bullhorn"></i> 需求大厅
        </h1>
        <p>浏览边疆需求与内地供给信息，精准匹配东西协作合作方向</p>
      </div>
    </section>

    <div class="container content-area">

      <!-- ========== 双向智能对接（自由输入）========== -->
      <div class="bidirect-panel">
        <div class="bp-head">
          <span class="bp-title">双向智能对接</span>
          <p class="bp-sub">不必从列表里挑——直接用一句话描述，系统替你翻遍全库</p>
        </div>
        <div class="bp-roles">
          <button class="bp-role" :class="{ on: bpRole === 'demand' }" @click="bpRole = 'demand'">
            <i class="fas fa-bullhorn"></i> 我是需求方
            <small>描述需求 → 匹配资源</small>
          </button>
          <button class="bp-role" :class="{ on: bpRole === 'supply' }" @click="bpRole = 'supply'">
            <i class="fas fa-handshake"></i> 我是供给方
            <small>输入能力画像 → 匹配需求</small>
          </button>
        </div>
        <div class="bp-input-row">
          <textarea
            v-model="bpText"
            class="bp-text"
            rows="2"
            :placeholder="bpRole === 'demand'
              ? '例：我们喀什的红枣丰收了但只能卖原料，想做深加工，需要技术和设备'
              : '例：我们是山大能源团队，擅长光伏电站控制、储能系统集成与运维培训'"
          ></textarea>
          <button class="bp-go" :disabled="bpLoading || !bpText.trim()" @click="runBidirect">
            <i class="fas" :class="bpLoading ? 'fa-spinner fa-spin' : 'fa-bolt'"></i>
            {{ bpLoading ? '匹配中' : '立即匹配' }}
          </button>
        </div>
      </div>

      <!-- Tab 栏 -->
      <div class="tab-bar">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="tab-btn"
          :class="{ active: activeTab === tab.key }"
          @click="switchTab(tab.key)"
        >
          <i :class="tab.icon"></i>
          {{ tab.label }}
          <span class="tab-count">{{ tab.count }}</span>
        </button>
      </div>

      <!-- ========== 边疆需求侧 ========== -->
      <template v-if="activeTab === 'borderDemands'">
        <div class="filter-container">
          <div class="filter-title">
            <i class="fas fa-filter"></i> 按省份筛选
          </div>
          <div class="category-filter">
            <button
              v-for="cat in borderCategories"
              :key="cat"
              class="category-btn"
              :class="{ active: selectedBdCategory === cat }"
              @click="selectBdCategory(cat)"
            >{{ cat }}</button>
          </div>
        </div>

        <div v-if="filteredBorderDemands.length > 0" class="results-info">
          <span>找到 <strong>{{ filteredBorderDemands.length }}</strong> 条边疆需求</span>
          <span>显示第 {{ bdDisplayRange }}</span>
        </div>

        <div v-if="filteredBorderDemands.length === 0" class="no-data">
          <i class="fas fa-folder-open no-data-icon"></i>
          <p>未找到匹配的边疆需求</p>
        </div>

        <main v-else class="demands-container">
          <article
            v-for="(item, index) in pagedBorderDemands"
            :key="item['需求ID']"
            class="demand-card border-demand-card"
          >
            <h2 class="demand-title">
              {{ item['需求标题'] }}
              <span class="status-tag bd-stage-tag">{{ item['需求阶段'] || '待定' }}</span>
              <span class="card-id">{{ item['需求ID'] }}</span>
            </h2>

            <div class="demand-info">
              <div class="info-item"><i class="fas fa-map-marker-alt"></i> {{ item['省/自治区'] || '未知' }}</div>
              <div class="info-item" v-if="item['地市/边境县/乡镇']"><i class="fas fa-location-arrow"></i> {{ truncateText(item['地市/边境县/乡镇'], 25) }}</div>
              <div class="info-item"><i class="fas fa-building"></i> {{ truncateText(item['需求发布方'], 30) }}</div>
            </div>

            <div v-if="item['适配供给标签']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-tag"></i> 适配供给标签</div>
              <div class="detail-block-content">{{ item['适配供给标签'] }}</div>
            </div>

            <div v-if="item['痛点/现状']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-exclamation-circle"></i> 痛点/现状</div>
              <div class="detail-block-content">{{ truncateText(item['痛点/现状'], 200) }}</div>
            </div>

            <div v-if="item['具体需求描述']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-file-alt"></i> 具体需求描述</div>
              <div class="detail-block-content">{{ truncateText(item['具体需求描述'], 200) }}</div>
            </div>

            <div v-if="item['预期目标及合作方式']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-bullseye"></i> 预期目标及合作方式</div>
              <div class="detail-block-content">{{ truncateText(item['预期目标及合作方式'], 150) }}</div>
            </div>

            <div class="contact-info">
              <div class="contact-details">
                <span class="contact-name">{{ truncateText(item['需求发布方'], 25) }}</span>
                <div class="contact-tags">
                  <span class="contact-tag">{{ item['省/自治区'] || '未知' }}</span>
                  <span class="contact-tag">{{ item['需求阶段'] || '待定' }}</span>
                </div>
              </div>
              <div class="contact-btns">
                <button class="match-btn" @click="runMatchSupplies(item)">
                  <i class="fas fa-magic"></i> 智能匹配供给方
                </button>
                <button class="contact-btn" @click="openDetail(item, 'demand')">
                  <i class="fas fa-eye"></i> 查看详情
                </button>
              </div>
            </div>

            <hr v-if="index < pagedBorderDemands.length - 1" class="divider" />
          </article>
        </main>

        <div v-if="bdTotalPages > 1" class="pagination-container">
          <div class="pagination">
            <button class="page-btn" :class="{ disabled: bdPage === 1 }" @click="changeBdPage(-1)">
              <i class="fas fa-chevron-left"></i>
            </button>
            <span class="page-info">第 {{ bdPage }} 页 / 共 {{ bdTotalPages }} 页 ({{ filteredBorderDemands.length }} 条)</span>
            <button class="page-btn" :class="{ disabled: bdPage === bdTotalPages }" @click="changeBdPage(1)">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </template>

      <!-- ========== 内地供给侧 ========== -->
      <template v-if="activeTab === 'mainlandSupply'">
        <div class="filter-container">
          <div class="filter-title">
            <i class="fas fa-filter"></i> 按主体类型筛选
          </div>
          <div class="category-filter">
            <button
              v-for="cat in supplyCategories"
              :key="cat"
              class="category-btn supply-cat-btn"
              :class="{ active: selectedMsCategory === cat }"
              @click="selectMsCategory(cat)"
            >{{ cat }}</button>
          </div>
        </div>

        <div v-if="filteredMainlandSupply.length > 0" class="results-info">
          <span>找到 <strong>{{ filteredMainlandSupply.length }}</strong> 条供给信息</span>
          <span>显示第 {{ msDisplayRange }}</span>
        </div>

        <div v-if="filteredMainlandSupply.length === 0" class="no-data">
          <i class="fas fa-folder-open no-data-icon"></i>
          <p>未找到匹配的供给信息</p>
        </div>

        <main v-else class="demands-container">
          <article
            v-for="(item, index) in pagedMainlandSupply"
            :key="item['供给ID']"
            class="demand-card supply-demand-card"
          >
            <h2 class="demand-title">
              {{ truncateText(item['提供方'], 35) }}
              <span class="status-tag ms-type-tag">{{ item['主体类型'] || '未知' }}</span>
              <span class="card-id">{{ item['供给ID'] }}</span>
            </h2>

            <div class="demand-info">
              <div class="info-item"><i class="fas fa-map-marker-alt"></i> {{ item['所在地'] || '未知' }}</div>
              <div class="info-item" v-if="item['合作交付方式']"><i class="fas fa-handshake"></i> {{ truncateText(item['合作交付方式'], 25) }}</div>
            </div>

            <div v-if="item['可提供服务']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-concierge-bell"></i> 可提供服务</div>
              <div class="detail-block-content">{{ truncateText(item['可提供服务'], 200) }}</div>
            </div>

            <div v-if="item['核心技术优势']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-cogs"></i> 核心技术优势</div>
              <div class="detail-block-content">{{ truncateText(item['核心技术优势'], 150) }}</div>
            </div>

            <div v-if="item['应用场景与案例']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-lightbulb"></i> 应用场景与案例</div>
              <div class="detail-block-content">{{ truncateText(item['应用场景与案例'], 150) }}</div>
            </div>

            <div v-if="item['适配边疆需求']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-link"></i> 适配边疆需求</div>
              <div class="detail-block-content">{{ truncateText(item['适配边疆需求'], 150) }}</div>
            </div>

            <div class="contact-info">
              <div class="contact-details">
                <span class="contact-name">{{ truncateText(item['提供方'], 25) }}</span>
                <div class="contact-tags">
                  <span class="contact-tag">{{ item['所在地'] || '未知' }}</span>
                  <span class="contact-tag">{{ item['主体类型'] || '未知' }}</span>
                </div>
              </div>
              <div class="contact-btns">
                <button class="match-btn match-demand-btn" @click="runMatchDemands(item)">
                  <i class="fas fa-bullseye"></i> 智能匹配需求
                </button>
                <button class="contact-btn supply-contact-btn" @click="openDetail(item, 'supply')">
                  <i class="fas fa-eye"></i> 查看详情
                </button>
              </div>
            </div>

            <hr v-if="index < pagedMainlandSupply.length - 1" class="divider" />
          </article>
        </main>

        <div v-if="msTotalPages > 1" class="pagination-container">
          <div class="pagination">
            <button class="page-btn" :class="{ disabled: msPage === 1 }" @click="changeMsPage(-1)">
              <i class="fas fa-chevron-left"></i>
            </button>
            <span class="page-info">第 {{ msPage }} 页 / 共 {{ msTotalPages }} 页 ({{ filteredMainlandSupply.length }} 条)</span>
            <button class="page-btn" :class="{ disabled: msPage === msTotalPages }" @click="changeMsPage(1)">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </template>

      <!-- 详情弹窗 -->
      <transition name="modal">
        <div v-if="selectedItem" class="modal-overlay" @click.self="closeDetail">
          <div class="modal-container">
            <button class="modal-close" @click="closeDetail"><i class="fas fa-times"></i></button>

            <div v-if="detailType === 'demand'" class="modal-content">
              <h2 class="modal-title">{{ selectedItem['需求标题'] }}</h2>
              <div class="modal-tags">
                <span class="modal-tag" v-if="selectedItem['需求阶段']">{{ selectedItem['需求阶段'] }}</span>
                <span class="modal-tag">{{ selectedItem['需求ID'] }}</span>
              </div>
              <div class="modal-grid">
                <div class="modal-field"><label>省/自治区</label><p>{{ selectedItem['省/自治区'] || '未提供' }}</p></div>
                <div class="modal-field"><label>地市/边境县/乡镇</label><p>{{ selectedItem['地市/边境县/乡镇'] || '未提供' }}</p></div>
                <div class="modal-field"><label>需求发布方</label><p>{{ selectedItem['需求发布方'] || '未提供' }}</p></div>
                <div class="modal-field"><label>适配供给标签</label><p>{{ selectedItem['适配供给标签'] || '未提供' }}</p></div>
              </div>
              <div class="modal-section" v-if="selectedItem['痛点/现状']"><h4>痛点/现状</h4><p>{{ selectedItem['痛点/现状'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['具体需求描述']"><h4>具体需求描述</h4><p>{{ selectedItem['具体需求描述'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['预期目标及合作方式']"><h4>预期目标及合作方式</h4><p>{{ selectedItem['预期目标及合作方式'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['原文链接']"><h4>原文链接</h4><a :href="selectedItem['原文链接']" target="_blank" class="source-link">{{ selectedItem['原文链接'] }}</a></div>
            </div>

            <div v-else-if="detailType === 'supply'" class="modal-content">
              <h2 class="modal-title">{{ selectedItem['提供方'] }}</h2>
              <div class="modal-tags">
                <span class="modal-tag" v-if="selectedItem['主体类型']">{{ selectedItem['主体类型'] }}</span>
                <span class="modal-tag">{{ selectedItem['供给ID'] }}</span>
              </div>
              <div class="modal-grid">
                <div class="modal-field"><label>所在地</label><p>{{ selectedItem['所在地'] || '未提供' }}</p></div>
                <div class="modal-field"><label>主体类型</label><p>{{ selectedItem['主体类型'] || '未提供' }}</p></div>
              </div>
              <div class="modal-section" v-if="selectedItem['可提供服务']"><h4>可提供服务</h4><p>{{ selectedItem['可提供服务'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['核心技术优势']"><h4>核心技术优势</h4><p>{{ selectedItem['核心技术优势'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['应用场景与案例']"><h4>应用场景与案例</h4><p>{{ selectedItem['应用场景与案例'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['适配边疆需求']"><h4>适配边疆需求</h4><p>{{ selectedItem['适配边疆需求'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['合作交付方式']"><h4>合作交付方式</h4><p>{{ selectedItem['合作交付方式'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['官网/案例链接']"><h4>官网/案例链接</h4><a :href="selectedItem['官网/案例链接']" target="_blank" class="source-link">{{ selectedItem['官网/案例链接'] }}</a></div>
            </div>
          </div>
        </div>
      </transition>

      <!-- 智能匹配弹窗 -->
      <transition name="modal">
        <div v-if="matchingLoading || matchingResult" class="modal-overlay" @click.self="closeMatching">
          <div class="modal-container matching-modal">
            <button class="modal-close" @click="closeMatching"><i class="fas fa-times"></i></button>

            <!-- 加载中 -->
            <div v-if="matchingLoading" class="matching-loading">
              <div class="spinner"></div>
              <p>正在智能匹配中...</p>
              <p class="matching-subtitle">{{ matchingTitle }}</p>
            </div>

            <!-- 匹配结果 -->
            <div v-else-if="matchingResult && !matchingResult.error" class="modal-content">
              <h2 class="modal-title">
                <i class="fas fa-magic matching-title-icon"></i>
                智能匹配结果
              </h2>
              <p class="matching-source">{{ matchingTitle }}</p>

              <div class="matching-summary">
                <span class="match-summary-item">
                  <i class="fas fa-filter"></i> 候选 {{ matchingResult.filter_info?.candidate_count || 0 }}
                </span>
                <span class="match-summary-item">
                  <i class="fas fa-check-circle"></i> 匹配 {{ matchingResult.total || 0 }}
                </span>
                <span class="match-summary-item" v-if="matchingResult.filter_info?.subject_type">
                  <i class="fas fa-tag"></i> {{ matchingResult.filter_info.subject_type }}
                </span>
                <span class="match-summary-item" v-if="matchingResult.filter_info?.province && !matchingResult.is_v2">
                  <i class="fas fa-map-marker-alt"></i> {{ matchingResult.filter_info.province }}
                </span>
                <template v-if="matchingResult.is_v2">
                  <span class="match-summary-item v2-badge">
                    <i class="fas fa-layer-group"></i> L1 {{ matchingResult.filter_info.candidate_count }}
                  </span>
                  <span class="match-summary-item v2-badge">
                    <i class="fas fa-check-double"></i> L2 {{ matchingResult.filter_info.matched_count }}
                  </span>
                  <span class="match-summary-item v2-badge" :class="{ llm: matchingResult.filter_info.judge_mode === 'llm' }">
                    <i class="fas fa-brain"></i> {{ matchingResult.filter_info.judge_mode === 'llm' ? 'DeepSeek 研判' : '规则模式' }}
                  </span>
                </template>
              </div>

              <!-- 历史范式参考 -->
              <div v-if="matchingResult.is_v2 && matchingResult.history_reference?.length" class="history-reference">
                <h4 class="hr-title"><i class="fas fa-history"></i> 历史范式参考 · 已完成成果可复制协作点</h4>
                <div v-for="(r, ri) in matchingResult.history_reference" :key="ri" class="hr-card">
                  <p class="hr-name">{{ r.title }}</p>
                  <p class="hr-meta">{{ r.region }}　|　可复制点：{{ r.replicable_points }}</p>
                </div>
              </div>

              <div v-if="matchingResult.matches && matchingResult.matches.length > 0" class="match-results">
                <div
                  v-for="(m, idx) in matchingResult.matches"
                  :key="idx"
                  class="match-card"
                  :class="matchingType === 'demand' ? 'match-supply-card' : 'match-demand-card'"
                >
                  <div class="match-rank">#{{ idx + 1 }}</div>
                  <div class="match-card-body">
                    <h3 class="match-card-title">
                      {{ matchingType === 'demand' ? m.supply.provider : m.demand.title }}
                    </h3>
                    <div class="match-card-meta">
                      <span v-if="matchingType === 'demand'" class="match-meta-item">
                        <i class="fas fa-map-marker-alt"></i> {{ m.supply.location || '未知' }}
                      </span>
                      <span v-if="matchingType === 'demand'" class="match-meta-item">
                        <i class="fas fa-building"></i> {{ m.supply.subject_type || '未知' }}
                      </span>
                      <span v-if="matchingType === 'demand'" class="match-meta-item">
                        <i class="fas fa-link"></i> {{ truncateText(m.supply.border_fit, 40) }}
                      </span>
                      <span v-if="matchingType === 'supply'" class="match-meta-item">
                        <i class="fas fa-map-marker-alt"></i> {{ m.demand.province || '未知' }}
                      </span>
                      <span v-if="matchingType === 'supply'" class="match-meta-item">
                        <i class="fas fa-flag"></i> {{ m.demand.stage || '待定' }}
                      </span>
                      <span v-if="matchingType === 'supply'" class="match-meta-item">
                        <i class="fas fa-tag"></i> {{ m.demand.supply_tags || '无标签' }}
                      </span>
                    </div>
                    <p v-if="matchingType === 'demand'" class="match-card-desc">
                      {{ truncateText(m.supply.services, 150) }}
                    </p>
                    <p v-else class="match-card-desc">
                      {{ truncateText(m.demand.pain_point || m.demand.description, 150) }}
                    </p>
                    <div class="match-scores">
                      <span class="score-badge total">综合 {{ m.score }}</span>
                      <template v-if="matchingResult.is_v2">
                        <span class="score-badge v2-tag" :class="m.candidate_type">
                          {{ m.candidate_type === 'talent' ? '山大人才' : (m.candidate_type === 'demand' ? '边疆需求' : '企业/机构') }}
                        </span>
                        <span class="score-badge">关键词 {{ m.keyword_score }}</span>
                        <span class="score-badge">标签 {{ m.tag_score }}</span>
                        <span class="score-badge" v-if="m.credibility != null" title="三因子：来源0.4+时效0.3+核验0.3">
                          可信度 {{ m.credibility }}
                        </span>
                      </template>
                      <template v-else>
                        <span class="score-badge">关键词 {{ m.keyword_score }}</span>
                        <span class="score-badge">标签 {{ m.tag_score }}</span>
                      </template>
                    </div>
                    <div v-if="m.llm_reason" class="llm-judge">
                      <p class="llm-row"><strong><i class="fas fa-brain"></i> 研判理由</strong>{{ truncateText(m.llm_reason, 180) }}</p>
                      <p class="llm-row" v-if="m.llm_risk"><strong><i class="fas fa-exclamation-triangle"></i> 风险提示</strong>{{ truncateText(m.llm_risk, 120) }}</p>
                      <p class="llm-row" v-if="m.llm_suggestion"><strong><i class="fas fa-lightbulb"></i> 对接建议</strong>{{ truncateText(m.llm_suggestion, 140) }}</p>
                    </div>
                    <div class="match-contact">
                      <i class="fas fa-address-card"></i>
                      <span class="mc-label">直接联系</span>
                      <span class="mc-value" v-if="m.contact">{{ truncateText(m.contact, 80) }}</span>
                      <span class="mc-value dim" v-else>暂无直接联系方式，见信源渠道</span>
                      <a v-if="m.source_url" :href="m.source_url" target="_blank" rel="noopener" class="mc-link">
                        <i class="fas fa-external-link-alt"></i> 信源原文
                      </a>
                      <button class="mc-chat-btn" @click="openContactDialog(m)">
                        <i class="fas fa-comments"></i> 发起对接
                      </button>
                    </div>
                    <div class="match-contact">
                      <i class="fas fa-address-card"></i>
                      <span class="mc-label">直接联系</span>
                      <span class="mc-value" v-if="m.contact">{{ truncateText(m.contact, 80) }}</span>
                      <span class="mc-value dim" v-else>暂无直接联系方式，见信源渠道</span>
                      <a v-if="m.source_url" :href="m.source_url" target="_blank" rel="noopener" class="mc-link">
                        <i class="fas fa-external-link-alt"></i> 信源原文
                      </a>
                      <button class="mc-chat-btn" @click="openContactDialog(m)">
                        <i class="fas fa-comments"></i> 发起对接
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="no-match-result">
                <i class="fas fa-search"></i>
                <p>未找到匹配结果</p>
              </div>
            </div>

            <!-- 错误提示 -->
            <div v-else-if="matchingResult && matchingResult.error" class="modal-content">
              <h2 class="modal-title"><i class="fas fa-exclamation-triangle"></i> 匹配失败</h2>
              <p class="error-message">{{ matchingResult.message }}</p>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 发起对接弹窗（全局单例） -->
    <transition name="modal">
      <div v-if="contactTarget" class="modal-overlay" @click.self="contactTarget = null">
        <div class="modal-container contact-modal">
          <button class="modal-close" @click="contactTarget = null"><i class="fas fa-times"></i></button>
          <div class="modal-content">
            <h2 class="modal-title"><i class="fas fa-comments"></i> 发起对接</h2>
            <p class="cm-subject">{{ contactTarget.provider }}</p>
            <div class="cm-contact-box">
              <p class="cm-row"><strong>官方渠道</strong>{{ contactTarget.contact || '暂无直接联系方式，建议通过信源渠道对接' }}</p>
              <a v-if="contactTarget.source_url" :href="contactTarget.source_url" target="_blank" rel="noopener" class="cm-link">
                <i class="fas fa-external-link-alt"></i> 查看信源原文
              </a>
            </div>
            <template v-if="authStore.isLoggedIn">
              <textarea v-model="contactMessage" class="cm-text" rows="3"
                placeholder="写一句对接意向，发送后将进入「对接中心」会话，可持续沟通"></textarea>
              <div class="cm-actions">
                <button class="cm-send" :disabled="contactSending || !contactMessage.trim()" @click="sendContact">
                  <i class="fas" :class="contactSending ? 'fa-spinner fa-spin' : 'fa-paper-plane'"></i>
                  {{ contactSending ? '发送中' : '发送对接意向' }}
                </button>
              </div>
            </template>
            <div v-else class="cm-login-tip">
              登录后可在平台内发送对接意向并持续沟通。
              <router-link to="/login" class="cm-login-link">去登录</router-link>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { ref, computed, onMounted, watch } from 'vue'
import { matchSuppliesForDemand, matchDemandsForSupply, matchDemandV2, freestyleMatch, reverseMatch } from '@/api/matching'
import { startThread } from '@/api/contact'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'



const authStore = useAuthStore()

/* ---------- 发起对接 ---------- */
const contactTarget = ref(null)
const contactMessage = ref('')
const contactSending = ref(false)

const openContactDialog = (m) => {
  if (!authStore.isLoggedIn) {
    ElMessage.warning('请先登录后再发起对接')
  }
  contactTarget.value = m
  contactMessage.value = `您好！我对「${(m.provider || '').slice(0, 30)}」很感兴趣，希望进一步沟通对接事宜。`
}

const sendContact = async () => {
  if (!contactTarget.value || !contactMessage.value.trim()) return
  contactSending.value = true
  try {
    await startThread({
      subject_type: contactTarget.value.candidate_type === 'demand' ? 'demand'
                  : contactTarget.value.candidate_type === 'talent' ? 'talent' : 'supply',
      subject_id: contactTarget.value.supply_id || contactTarget.value.supply?.provider || null,
      subject_title: contactTarget.value.provider || '',
      entity_contact: contactTarget.value.contact || '',
      entity_link: contactTarget.value.source_url || '',
      message: contactMessage.value.trim(),
    })
    ElMessage.success('对接意向已发送，可在「对接中心」查看会话')
    contactTarget.value = null
    contactMessage.value = ''
  } catch (e) {
    console.error('发送失败:', e)
    ElMessage.error(e?.response?.data?.detail || '发送失败，请重试')
  } finally {
    contactSending.value = false
  }
}

/* ---------- 双向智能对接 ---------- */
const bpRole = ref('demand')
const bpText = ref('')
const bpLoading = ref(false)

const runBidirect = async () => {
  if (!bpText.value.trim() || bpLoading.value) return
  bpLoading.value = true
  matchingLoading.value = true
  matchingTitle.value = bpRole.value === 'demand' ? '自由需求 · 双向对接' : '能力画像 · 双向对接'
  try {
    const res = bpRole.value === 'demand'
      ? await freestyleMatch(bpText.value.trim(), { top_k: 5, use_llm: true })
      : await reverseMatch(bpText.value.trim(), { top_k: 5, use_llm: true })
    const fi = res.filter_info || {}
    matchingResult.value = {
      demand: res.demand || { title: res.capability_text, province: '', publisher: '能力画像', supply_tags: '', pain_point: res.capability_text },
      total: res.total,
      filter_info: {
        candidate_count: fi.level1_candidates ?? 0,
        matched_count: fi.level2_matched ?? 0,
        judge_mode: fi.judge_mode || 'rule',
        mode: res.mode,
      },
      history_reference: res.history_reference || [],
      is_v2: true,
      matches: (res.matches || []).map(m => ({
        score: m.score,
        keyword_score: m.keyword_score,
        tag_score: m.tag_score,
        credibility: m.credibility,
        source_weight: m.source_weight,
        timeliness: m.timeliness,
        verification: m.verification,
        candidate_type: m.candidate_type || 'enterprise',
        llm_reason: m.llm_match_reason,
        llm_risk: m.llm_risk,
        llm_suggestion: m.llm_suggestion,
        judge_mode: m.judge_mode,
        final_score: m.final_score,
        contact: m.contact,
        source_url: m.source_url,
        contact: m.contact,
        source_url: m.source_url,
        supply: {
          provider: m.provider || m.title,
          location: m.location || m.province,
          subject_type: m.subject_type || (m.candidate_type === 'demand' ? '边疆需求' : ''),
          border_fit: m.border_fit || m.pain_point,
          services: m.services || m.description,
        },
        demand: {},
      })),
    }
  } catch (e) {
    console.error('双向匹配失败:', e)
    matchingResult.value = { error: true, message: '匹配请求失败，请检查后端服务是否运行' }
  } finally {
    bpLoading.value = false
    matchingLoading.value = false
  }
}

/* ---------- Tab 切换 ---------- */
const activeTab = ref('borderDemands')
const itemsPerPage = 5

/* ---------- 边疆需求 & 内地供给状态 ---------- */
const borderDemands = ref([])
const mainlandSupply = ref([])
const selectedBdCategory = ref('全部')
const selectedMsCategory = ref('全部')
const bdPage = ref(1)
const msPage = ref(1)

const selectedItem = ref(null)
const detailType = ref('')

/* ---------- 智能匹配状态 ---------- */
const matchingLoading = ref(false)
const matchingResult = ref(null)
const matchingType = ref('')
const matchingTitle = ref('')

const tabs = computed(() => [
  { key: 'borderDemands', label: '边疆需求侧', icon: 'fas fa-flag', count: borderDemands.value.length },
  { key: 'mainlandSupply', label: '内地供给侧', icon: 'fas fa-hand-holding-heart', count: mainlandSupply.value.length }
])

const borderCategories = computed(() => {
  const ps = new Set(['全部'])
  borderDemands.value.forEach(d => {
    if (d['省/自治区']) ps.add(d['省/自治区'])
  })
  return Array.from(ps)
})

const supplyCategories = computed(() => {
  const ts = new Set(['全部'])
  mainlandSupply.value.forEach(s => {
    if (s['主体类型']) ts.add(s['主体类型'])
  })
  return Array.from(ts)
})

const filteredBorderDemands = computed(() => {
  if (selectedBdCategory.value === '全部') return borderDemands.value
  return borderDemands.value.filter(d => d['省/自治区'] === selectedBdCategory.value)
})

const filteredMainlandSupply = computed(() => {
  if (selectedMsCategory.value === '全部') return mainlandSupply.value
  return mainlandSupply.value.filter(s => s['主体类型'] === selectedMsCategory.value)
})

const bdTotalPages = computed(() => Math.ceil(filteredBorderDemands.value.length / itemsPerPage) || 1)
const msTotalPages = computed(() => Math.ceil(filteredMainlandSupply.value.length / itemsPerPage) || 1)

const bdDisplayRange = computed(() => {
  if (pagedBorderDemands.value.length === 0) return '0-0'
  const start = (bdPage.value - 1) * itemsPerPage + 1
  const end = start + pagedBorderDemands.value.length - 1
  return `${start}-${end}`
})

const msDisplayRange = computed(() => {
  if (pagedMainlandSupply.value.length === 0) return '0-0'
  const start = (msPage.value - 1) * itemsPerPage + 1
  const end = start + pagedMainlandSupply.value.length - 1
  return `${start}-${end}`
})

const pagedBorderDemands = computed(() => {
  const start = (bdPage.value - 1) * itemsPerPage
  return filteredBorderDemands.value.slice(start, start + itemsPerPage)
})

const pagedMainlandSupply = computed(() => {
  const start = (msPage.value - 1) * itemsPerPage
  return filteredMainlandSupply.value.slice(start, start + itemsPerPage)
})

/* ---------- 方法 ---------- */
const switchTab = (key) => {
  activeTab.value = key
  selectedBdCategory.value = '全部'
  selectedMsCategory.value = '全部'
  bdPage.value = 1
  msPage.value = 1
}

const changeBdPage = (delta) => {
  const next = bdPage.value + delta
  if (next >= 1 && next <= bdTotalPages.value) {
    bdPage.value = next
    window.scrollTo({ top: 300, behavior: 'smooth' })
  }
}

const changeMsPage = (delta) => {
  const next = msPage.value + delta
  if (next >= 1 && next <= msTotalPages.value) {
    msPage.value = next
    window.scrollTo({ top: 300, behavior: 'smooth' })
  }
}

const selectBdCategory = (cat) => {
  selectedBdCategory.value = cat
  bdPage.value = 1
}

const selectMsCategory = (cat) => {
  selectedMsCategory.value = cat
  msPage.value = 1
}

const truncateText = (text, max) => {
  if (!text) return ''
  if (text.length <= max) return text
  return text.substring(0, max) + '...'
}

const openDetail = (item, type) => {
  selectedItem.value = item
  detailType.value = type
  document.body.style.overflow = 'hidden'
}

const closeDetail = () => {
  selectedItem.value = null
  document.body.style.overflow = ''
}

/* ---------- 智能匹配 ---------- */
const runMatchSupplies = async (item) => {
  matchingLoading.value = true
  matchingResult.value = null
  matchingType.value = 'demand'
  matchingTitle.value = item['需求标题'] || item['需求ID']
  document.body.style.overflow = 'hidden'
  try {
    const res = await matchDemandV2(item['需求ID'], { top_k: 5, use_llm: true })
    // 适配 v2 三级漏斗结构：保留旧模板字段 + 挂载新能力
    const fi = res.filter_info || {}
    matchingResult.value = {
      demand: res.demand,
      total: res.total,
      filter_info: {
        candidate_count: fi.level1_candidates ?? 0,
        matched_count: fi.level2_matched ?? 0,
        judge_mode: fi.judge_mode || 'rule',
      },
      history_reference: res.history_reference || [],
      is_v2: true,
      matches: (res.matches || []).map(m => ({
        score: m.final_score ?? m.score,
        keyword_score: m.keyword_score,
        tag_score: m.tag_score,
        credibility: m.credibility,
        source_weight: m.source_weight,
        timeliness: m.timeliness,
        verification: m.verification,
        candidate_type: m.candidate_type || 'enterprise',
        llm_reason: m.llm_match_reason,
        llm_risk: m.llm_risk,
        llm_suggestion: m.llm_suggestion,
        judge_mode: m.judge_mode,
        contact: m.contact,
        source_url: m.source_url,
        contact: m.contact,
        source_url: m.source_url,
        supply: {
          provider: m.provider,
          location: m.location,
          subject_type: m.subject_type,
          border_fit: m.border_fit,
          services: m.services,
        },
        demand: {},
      })),
    }
  } catch (e) {
    console.error('匹配失败:', e)
    matchingResult.value = { error: true, message: '匹配请求失败，请检查后端服务是否运行' }
  } finally {
    matchingLoading.value = false
  }
}

const runMatchDemands = async (item) => {
  matchingLoading.value = true
  matchingResult.value = null
  matchingType.value = 'supply'
  matchingTitle.value = item['提供方'] || item['供给ID']
  document.body.style.overflow = 'hidden'
  try {
    const res = await matchDemandsForSupply(item['供给ID'], { top_k: 5 })
    matchingResult.value = res
  } catch (e) {
    console.error('匹配失败:', e)
    matchingResult.value = { error: true, message: '匹配请求失败，请检查后端服务是否运行' }
  } finally {
    matchingLoading.value = false
  }
}

const closeMatching = () => {
  matchingResult.value = null
  matchingLoading.value = false
  matchingType.value = ''
  matchingTitle.value = ''
  document.body.style.overflow = ''
}

watch(selectedBdCategory, () => { bdPage.value = 1 })
watch(selectedMsCategory, () => { msPage.value = 1 })

onMounted(async () => {
  try {
    const res = await fetch('/data/achievements.json')
    const data = await res.json()
    borderDemands.value = data.border_demands || []
    mainlandSupply.value = data.mainland_supply || []
  } catch (e) {
    console.error('加载案例数据失败:', e)
  }
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: var(--paper);
}

.page-header {
  background: var(--paper-2);
  color: var(--ink);
  padding: 46px 5% 38px;
  text-align: center;
  border-bottom: 3px double var(--ink);
}

.page-header h1 {
  font-size: 2.8rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.page-header p {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 800px;
  margin: 0 auto;
}

.content-area {
  padding: 30px 5% 60px;
}

.filter-container {
  background: var(--color-bg-card, #fff);
  border-radius: 12px;
  padding: 25px 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.filter-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-title i {
  color: var(--color-primary);
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.category-btn {
  padding: 10px 20px;
  background-color: var(--paper-2);
  border: 2px solid var(--color-border);
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  color: var(--ink-2);
  transition: all 0.3s;
}

.category-btn:hover {
  background-color: #e8e8e8;
  border-color: #bbb;
}

.category-btn.active {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.filter-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 25px;
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.95rem;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(41, 128, 185, 0.3);
}

.reset-btn {
  padding: 10px 20px;
  background-color: var(--paper-2);
  border: 2px solid var(--color-border);
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.95rem;
  color: var(--ink-2);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.reset-btn:hover {
  background-color: var(--paper-2);
}

.results-info {
  margin-bottom: 25px;
  padding: 15px 20px;
  background-color: var(--color-primary-light);
  border-radius: 8px;
  color: var(--color-primary-dark);
  font-weight: 500;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.demands-container {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.demand-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border-left: 6px solid var(--color-primary);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.demand-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.demand-title {
  color: var(--color-primary-dark);
  font-size: 1.8rem;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.demand-info {
  display: flex;
  gap: 30px;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--paper-2);
  flex-wrap: wrap;
}

.info-item {
  font-size: 1.05rem;
  color: var(--ink-2);
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-item i {
  color: var(--color-primary);
}

.majors-section {
  background-color: var(--paper-2);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
}

.majors-title {
  font-size: 1.2rem;
  color: var(--ink);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.majors-title i {
  color: var(--color-primary);
}

.majors-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.major-tag {
  background-color: var(--color-primary-light);
  color: var(--color-primary);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
}

.no-majors {
  color: var(--ink-3);
  font-style: italic;
  font-size: 0.9rem;
}

.demand-content {
  margin-bottom: 25px;
  color: var(--ink-2);
  line-height: 1.7;
  padding: 15px 20px;
  background-color: var(--paper-2);
  border-radius: 8px;
  border-left: 4px solid var(--color-primary);
}

.content-title {
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--ink);
}

.content-title i {
  color: var(--color-primary);
}

.contact-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px dashed var(--color-border);
  flex-wrap: wrap;
  gap: 15px;
}

.contact-details {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.contact-name {
  font-size: 1.3rem;
  font-weight: bold;
  color: var(--color-primary-dark);
}

.contact-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.contact-tag {
  background-color: var(--color-primary-light);
  color: var(--color-primary-dark);
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
}

.contact-btn {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 5px 15px rgba(41, 128, 185, 0.3);
  transition: background 0.2s, transform 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(41, 128, 185, 0.4);
}

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, var(--color-primary), transparent);
  margin: 30px 0;
  border: none;
}

.status-tag {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
}

.status-open {
  background-color: rgba(47,107,79,.08);
  color: #2f6b4f;
}

.status-closed {
  background-color: var(--color-accent-light);
  color: var(--color-accent);
}

.loading {
  text-align: center;
  padding: 60px;
  color: var(--ink-3);
}

.spinner {
  border: 4px solid var(--color-border);
  border-top: 4px solid var(--color-primary);
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-box {
  text-align: center;
  padding: 50px;
  color: var(--color-accent);
  background-color: var(--color-accent-light);
  border-radius: 12px;
  margin: 20px 0;
}

.error-box i {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: var(--color-accent);
}

.error-box p {
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.reload-btn {
  padding: 10px 24px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background 0.2s;
}

.reload-btn:hover {
  background: var(--color-primary-dark);
}

.no-data {
  text-align: center;
  padding: 60px;
  color: var(--ink-3);
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  margin: 20px 0;
}

.no-data i {
  font-size: 4rem;
  margin-bottom: 20px;
  color: var(--rule);
}

.no-data h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: var(--ink);
}

.no-data p {
  color: var(--ink-3);
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

.pagination {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}

.page-btn {
  padding: 8px 16px;
  background-color: #fff;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
  min-width: 40px;
  text-align: center;
  color: var(--ink-2);
}

.page-btn:hover:not(.disabled) {
  background-color: var(--paper-2);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.page-btn.active {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.page-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: var(--paper-2);
}

.page-info {
  color: var(--ink-3);
  font-size: 0.9rem;
  margin: 0 12px;
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2.2rem;
    flex-direction: column;
    gap: 10px;
  }

  .page-header p {
    font-size: 1rem;
  }

  .category-filter {
    justify-content: center;
  }

  .category-btn {
    padding: 8px 16px;
    font-size: 0.9rem;
  }

  .filter-actions {
    justify-content: center;
  }

  .demand-info {
    flex-direction: column;
    gap: 10px;
  }

  .contact-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .contact-btn {
    align-self: stretch;
    text-align: center;
    justify-content: center;
  }

  .pagination {
    flex-wrap: wrap;
    justify-content: center;
  }

  .page-info {
    order: -1;
    width: 100%;
    text-align: center;
    margin-bottom: 10px;
  }

  .demand-card {
    padding: 20px;
  }

  .demand-title {
    font-size: 1.4rem;
  }
}

/* ---------- Tab 栏 ---------- */
.tab-bar {
  display: flex;
  gap: 5px;
  margin-bottom: 25px;
  background: var(--color-primary-light);
  border-radius: 12px;
  padding: 6px;
}

.tab-btn {
  flex: 1;
  padding: 14px 20px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  color: var(--ink-2);
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.tab-btn.active {
  background: white;
  color: var(--color-primary);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.tab-count {
  background: var(--color-primary)22;
  color: var(--color-primary);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.tab-btn.active .tab-count {
  background: var(--color-primary);
  color: white;
}

/* ---------- 搜索与筛选工具栏 ---------- */
.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 200px;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--ink-3);
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 42px;
  border: 2px solid var(--color-border);
  border-radius: 10px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: var(--color-primary);
  outline: none;
}

.filter-select {
  padding: 12px 16px;
  border: 2px solid var(--color-border);
  border-radius: 10px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  min-width: 140px;
}

.filter-select:focus {
  border-color: var(--color-primary);
  outline: none;
}

/* ---------- 边疆需求 & 内地供给卡片 ---------- */
.card-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.case-card {
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid var(--paper-2);
}

.case-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

.demand-side-card {
  border-left: 6px solid var(--color-primary);
}

.supply-side-card {
  border-left: 6px solid var(--el-color-success);
}

.card-body {
  padding: 18px 22px;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.78rem;
  font-weight: 600;
}

.tag-demand {
  background: var(--color-primary)22;
  color: var(--color-primary);
}

.tag-supply {
  background: var(--el-color-success)22;
  color: var(--el-color-success);
}

.card-id {
  font-size: 0.8rem;
  color: var(--ink-3);
  font-weight: 500;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 10px;
  line-height: 1.4;
}

.card-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 0.85rem;
  color: var(--ink-3);
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-highlight {
  font-size: 0.9rem;
  color: var(--ink-2);
  line-height: 1.6;
  margin-bottom: 10px;
}

.card-sub {
  font-size: 0.85rem;
  color: #888;
  line-height: 1.5;
  margin-bottom: 10px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid var(--paper-2);
}

.view-detail {
  font-size: 0.85rem;
  color: var(--color-primary);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: gap 0.3s;
}

.case-card:hover .view-detail {
  gap: 8px;
}

.no-data-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  color: var(--rule);
}

/* ---------- 详情弹窗 ---------- */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  overflow-y: auto;
}

.modal-container {
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  padding: 35px;
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 36px;
  height: 36px;
  border: none;
  background: #f5f5f5;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.1rem;
  color: var(--ink-2);
  transition: all 0.3s;
  z-index: 1;
}

.modal-close:hover {
  background: var(--color-primary);
  color: white;
}

.modal-content {
  width: 100%;
}

.modal-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 12px;
  line-height: 1.4;
}

.modal-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.modal-tag {
  padding: 4px 12px;
  border-radius: 14px;
  font-size: 0.82rem;
  font-weight: 600;
  background: var(--color-primary)22;
  color: var(--color-primary);
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.modal-field label {
  font-size: 0.82rem;
  color: var(--ink-3);
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
}

.modal-field p {
  font-size: 0.95rem;
  color: var(--ink);
  line-height: 1.5;
}

.modal-section {
  margin-bottom: 18px;
}

.modal-section h4 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 6px;
  padding-bottom: 4px;
  border-bottom: 2px solid var(--color-primary)33;
}

.modal-section p {
  font-size: 0.92rem;
  color: var(--ink-2);
  line-height: 1.7;
}

.source-link {
  color: var(--color-primary);
  font-size: 0.88rem;
  word-break: break-all;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* ---------- 边疆需求/内地供给 卡片样式 ---------- */
.border-demand-card {
  border-left: 6px solid var(--color-primary);
}

.supply-demand-card {
  border-left: 6px solid var(--el-color-success);
}

.card-id {
  font-size: 0.8rem;
  color: var(--ink-3);
  font-weight: 500;
  margin-left: auto;
}

.bd-stage-tag {
  background-color: var(--color-primary-light);
  color: var(--color-primary-dark);
}

.ms-type-tag {
  background-color: rgba(47,107,79,.08);
  color: #2f6b4f;
}

.detail-block {
  margin-bottom: 14px;
  padding: 12px 16px;
  background-color: var(--paper-2);
  border-radius: 8px;
  border-left: 4px solid var(--color-primary);
}

.supply-demand-card .detail-block {
  border-left-color: var(--el-color-success);
}

.detail-block-label {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-block-label i {
  color: var(--color-primary);
}

.supply-demand-card .detail-block-label i {
  color: var(--el-color-success);
}

.detail-block-content {
  font-size: 0.9rem;
  color: var(--ink-2);
  line-height: 1.6;
}

.supply-cat-btn.active {
  background-color: var(--el-color-success);
  border-color: var(--el-color-success);
  color: white;
}

.supply-contact-btn {
  background: linear-gradient(135deg, #2f6b4f 0%, var(--el-color-success) 100%) !important;
  box-shadow: 0 5px 15px rgba(39, 174, 96, 0.3) !important;
}

.supply-contact-btn:hover {
  box-shadow: 0 8px 20px rgba(39, 174, 96, 0.4) !important;
}

@media (max-width: 768px) {
  .tab-btn {
    padding: 10px 12px;
    font-size: 0.85rem;
  }

  .toolbar {
    flex-direction: column;
  }

  .modal-grid {
    grid-template-columns: 1fr;
  }

  .modal-container {
    padding: 20px;
  }
}

/* ---------- 智能匹配按钮 ---------- */
.contact-btns {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.match-btn {
  background: linear-gradient(135deg, var(--talent) 0%, var(--talent) 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 0.95rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 5px 15px rgba(142, 36, 170, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.match-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(142, 36, 170, 0.4);
}

.match-demand-btn {
  background: linear-gradient(135deg, #245a3d 0%, #2f6b4f 100%);
  box-shadow: 0 5px 15px rgba(46, 125, 50, 0.3);
}

.match-demand-btn:hover {
  box-shadow: 0 8px 20px rgba(46, 125, 50, 0.4);
}

/* ---------- 智能匹配弹窗 ---------- */
.matching-modal {
  max-width: 720px;
}

.matching-loading {
  text-align: center;
  padding: 60px 20px;
}

.matching-loading p {
  color: var(--ink-2);
  font-size: 1.1rem;
  margin-top: 15px;
}

.matching-loading .matching-subtitle {
  color: var(--ink-3);
  font-size: 0.95rem;
  margin-top: 8px;
}

.matching-title-icon {
  color: var(--talent);
  margin-right: 8px;
}

.matching-source {
  color: var(--ink-2);
  font-size: 0.95rem;
  margin-bottom: 20px;
  padding: 10px 16px;
  background: var(--talent-bg);
  border-radius: 8px;
  border-left: 4px solid var(--talent);
}

.matching-summary {
  display: flex;
  gap: 16px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  padding: 12px 16px;
  background: var(--paper-2);
  border-radius: 10px;
}

.match-summary-item {
  font-size: 0.9rem;
  color: var(--ink);
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.match-summary-item i {
  color: var(--color-primary);
}

.match-results {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.match-card {
  display: flex;
  gap: 16px;
  padding: 18px;
  background: var(--paper-2);
  border-radius: 12px;
  border-left: 5px solid var(--talent);
  transition: box-shadow 0.3s, transform 0.3s;
}

.match-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  transform: translateX(4px);
}

.match-supply-card {
  border-left-color: var(--talent);
}

.match-demand-card {
  border-left-color: var(--el-color-success);
}

.match-rank {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--talent), var(--talent));
  color: white;
  font-weight: 700;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.match-demand-card .match-rank {
  background: linear-gradient(135deg, #245a3d, #2f6b4f);
}

.match-card-body {
  flex: 1;
  min-width: 0;
}

.match-card-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-primary-dark);
  margin-bottom: 8px;
  line-height: 1.4;
}

.match-card-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.match-meta-item {
  font-size: 0.82rem;
  color: var(--ink-3);
  display: flex;
  align-items: center;
  gap: 5px;
}

.match-meta-item i {
  color: var(--ink-3);
}

.match-card-desc {
  font-size: 0.88rem;
  color: var(--ink-2);
  line-height: 1.6;
  margin-bottom: 10px;
}

.match-scores {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.score-badge {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.78rem;
  font-weight: 600;
  background: var(--paper-2);
  color: var(--ink-2);
}

.score-badge.total {
  background: var(--talent)22;
  color: var(--talent);
  font-weight: 700;
}

.match-demand-card .score-badge.total {
  background: var(--el-color-success)22;
  color: var(--el-color-success);
}

.no-match-result {
  text-align: center;
  padding: 50px 20px;
  color: var(--ink-3);
}

.no-match-result i {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: var(--rule);
}

.error-message {
  color: var(--color-accent);
  font-size: 1rem;
  padding: 20px;
  background: var(--color-accent-light);
  border-radius: 8px;
  text-align: center;
}

@media (max-width: 768px) {
  .contact-btns {
    flex-direction: column;
    width: 100%;
  }

  .match-btn,
  .contact-btn {
    text-align: center;
    justify-content: center;
  }

  .match-card {
    flex-direction: column;
    gap: 10px;
  }

  .match-rank {
    align-self: flex-start;
  }
}
</style>

<style scoped>
/* ===== v2 三级漏斗 · 编辑风 ===== */
.v2-badge { color: var(--color-primary); }
.v2-badge.llm { color: #fff; background: var(--color-primary); font-weight: 650; padding: 3px 12px; border-radius: 3px; letter-spacing: 1px; }
.score-badge.v2-tag.talent { background: var(--talent-bg); color: var(--talent); border-color: rgba(109,76,159,.35); }
.score-badge.v2-tag.enterprise { background: rgba(30,58,110,.05); color: var(--color-primary); border-color: rgba(30,58,110,.3); }

.llm-judge {
  margin-top: 12px;
  padding: 12px 15px;
  background: var(--paper-2);
  border: none;
  border-left: 2px solid var(--color-primary);
  border-radius: 0 4px 4px 0;
}
.llm-judge .llm-row {
  margin: 5px 0;
  font-size: 12.8px;
  line-height: 1.8;
  color: var(--ink-2);
}
.llm-judge .llm-row strong {
  display: inline-block;
  margin-right: 10px;
  color: var(--color-primary);
  min-width: 78px;
  font-weight: 650;
}
.llm-judge .llm-row strong i { margin-right: 4px; }

.history-reference {
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px dashed var(--rule);
}
.hr-title {
  font-family: var(--font-serif);
  font-size: 13.5px;
  letter-spacing: 2px;
  color: var(--ink);
  margin-bottom: 12px;
  font-weight: 700;
}
.hr-title i { color: var(--color-accent); margin-right: 6px; }
.hr-card {
  padding: 10px 14px;
  margin-bottom: 8px;
  background: var(--color-bg-card);
  border-radius: 3px;
  border: 1px solid var(--color-border);
  border-left: 2px solid rgba(163,58,42,.35);
  transition: transform 0.3s var(--ease-out), border-color 0.25s;
}
.hr-card:hover { transform: translateX(4px); border-left-color: var(--color-accent); }
.hr-card .hr-name { font-size: 13px; font-weight: 650; color: var(--ink); margin-bottom: 3px; }
.hr-card .hr-meta { font-size: 12px; color: var(--ink-3); line-height: 1.7; }
</style>

<style scoped>
/* ===== 双向智能对接面板 · 编辑风 ===== */
.bidirect-panel {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-top: 3px solid var(--color-primary);
  border-radius: var(--radius-md);
  padding: 20px 24px;
  margin-bottom: 26px;
  box-shadow: var(--shadow-sm);
}
.bp-head { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; }
.bp-title {
  font-family: var(--font-serif);
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--ink);
}
.bp-sub { font-size: 12px; color: var(--ink-3); }

.bp-roles { display: flex; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
.bp-role {
  flex: 1; min-width: 220px;
  display: flex; flex-direction: column; align-items: flex-start; gap: 4px;
  padding: 12px 16px;
  background: var(--paper-2);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 14px; font-weight: 650; color: var(--ink);
  transition: transform 0.3s var(--ease-out), border-color 0.25s, background 0.25s;
}
.bp-role small { font-size: 11.5px; font-weight: 400; color: var(--ink-3); letter-spacing: 0.5px; }
.bp-role:hover { transform: translateY(-2px); border-color: var(--color-primary); }
.bp-role.on {
  background: var(--color-primary-light);
  border-color: var(--color-primary);
  color: var(--color-primary);
}
.bp-role.on small { color: var(--color-primary); opacity: 0.75; }

.bp-input-row { display: flex; gap: 12px; align-items: stretch; }
.bp-text {
  flex: 1;
  resize: vertical;
  min-height: 56px;
  padding: 10px 14px;
  font-size: 13.5px;
  line-height: 1.7;
  color: var(--ink);
  background: var(--paper);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-family);
}
.bp-text:focus { outline: none; border-color: var(--color-primary); }
.bp-go {
  align-self: flex-end;
  padding: 11px 26px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 650;
  letter-spacing: 1px;
  cursor: pointer;
  white-space: nowrap;
  transition: transform 0.25s var(--ease-out), box-shadow 0.25s var(--ease-out), background 0.2s;
}
.bp-go:hover:not(:disabled) {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(30, 58, 110, 0.25);
}
.bp-go:disabled { opacity: 0.45; cursor: not-allowed; }

@media (max-width: 640px) {
  .bp-input-row { flex-direction: column; }
  .bp-go { align-self: stretch; }
}
</style>

<style scoped>
/* ===== 匹配卡 · 直接联系行 ===== */
.match-contact {
  margin-top: 11px;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 9px;
  flex-wrap: wrap;
  background: var(--paper-2);
  border-left: 2px solid var(--el-color-success);
  border-radius: 0 4px 4px 0;
  font-size: 12.5px;
}
.match-contact i.fa-address-card { color: var(--el-color-success); }
.mc-label { font-weight: 650; color: var(--el-color-success); letter-spacing: 1px; white-space: nowrap; }
.mc-value { color: var(--ink-2); line-height: 1.6; word-break: break-all; }
.mc-value.dim { color: var(--ink-3); }
.mc-link {
  margin-left: auto;
  font-size: 12px;
  color: var(--color-primary);
  text-decoration: none;
  white-space: nowrap;
  border-bottom: 1px dashed rgba(30, 58, 110, 0.4);
}
.mc-link:hover { color: var(--color-primary-dark); border-bottom-style: solid; }
</style>

<style scoped>
/* ===== 匹配卡 · 直接联系行 ===== */
.match-contact {
  margin-top: 11px;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 9px;
  flex-wrap: wrap;
  background: var(--paper-2);
  border-left: 2px solid var(--el-color-success);
  border-radius: 0 4px 4px 0;
  font-size: 12.5px;
}
.match-contact i.fa-address-card { color: var(--el-color-success); }
.mc-label { font-weight: 650; color: var(--el-color-success); letter-spacing: 1px; white-space: nowrap; }
.mc-value { color: var(--ink-2); line-height: 1.6; word-break: break-all; }
.mc-value.dim { color: var(--ink-3); }
.mc-link {
  margin-left: auto;
  font-size: 12px;
  color: var(--color-primary);
  text-decoration: none;
  white-space: nowrap;
  border-bottom: 1px dashed rgba(30, 58, 110, 0.4);
}
.mc-link:hover { color: var(--color-primary-dark); border-bottom-style: solid; }
</style>

<style scoped>
/* ===== 发起对接按钮与弹窗 ===== */
.mc-chat-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 13px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 650;
  letter-spacing: 1px;
  cursor: pointer;
  white-space: nowrap;
  transition: transform 0.25s var(--ease-out), box-shadow 0.25s var(--ease-out), background 0.2s;
}
.mc-chat-btn:hover {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(30, 58, 110, 0.25);
}

.contact-modal { max-width: 520px; width: 92%; }
.cm-subject {
  font-family: var(--font-serif);
  font-size: 15px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 12px;
  line-height: 1.6;
}
.cm-contact-box {
  background: var(--paper-2);
  border-left: 2px solid var(--el-color-success);
  border-radius: 0 4px 4px 0;
  padding: 10px 13px;
  margin-bottom: 14px;
}
.cm-row { font-size: 12.8px; line-height: 1.75; color: var(--ink-2); margin-bottom: 4px; }
.cm-row strong { display: inline-block; min-width: 64px; color: var(--el-color-success); margin-right: 8px; }
.cm-link { font-size: 12px; color: var(--color-primary); text-decoration: none; }
.cm-link:hover { text-decoration: underline; }
.cm-text {
  width: 100%;
  resize: vertical;
  padding: 10px 13px;
  font-size: 13px;
  line-height: 1.7;
  color: var(--ink);
  background: var(--paper);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-family);
}
.cm-text:focus { outline: none; border-color: var(--color-primary); }
.cm-actions { margin-top: 12px; display: flex; justify-content: flex-end; }
.cm-send {
  padding: 9px 24px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 650;
  letter-spacing: 1px;
  cursor: pointer;
  transition: transform 0.25s var(--ease-out), box-shadow 0.25s var(--ease-out), background 0.2s;
}
.cm-send:hover:not(:disabled) {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 5px 14px rgba(30, 58, 110, 0.25);
}
.cm-send:disabled { opacity: 0.45; cursor: not-allowed; }
.cm-login-tip {
  font-size: 13px;
  color: var(--ink-2);
  background: var(--paper-2);
  padding: 12px 14px;
  border-radius: var(--radius-sm);
}
.cm-login-link { color: var(--color-primary); font-weight: 650; margin-left: 6px; }
</style>
